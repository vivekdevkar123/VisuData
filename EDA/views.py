from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Dataset,Note
from django.http import HttpResponse,FileResponse
import pandas as pd
import os
from django.conf import settings
from django.contrib import messages
from Visulization.models import Plot
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import base64
import json

# Create your views here.

@login_required(login_url='login')
def FileUpload(request):
    if request.method == 'POST':
        dataset_name = request.POST.get('dataset_name')
        uploaded_file = request.FILES.get('uploaded_file')
        user = request.user

        # Check if the file is either an Excel or CSV file
        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension not in ['csv']:
                return HttpResponse("Invalid file format. Only CSV files are allowed.")

        if dataset_name and uploaded_file:
            dataset = Dataset(user=user, dataset_name=dataset_name, uploaded_file=uploaded_file)
            dataset.save()
            return redirect('history') 


    return render(request, 'analysis/upload-file.html')


@login_required(login_url='login')
def History(request):
    datasets = Dataset.objects.filter(user = request.user)[::-1]
    context = {
        'datasets':datasets,
    }
    return render(request, 'analysis/history.html',context)


@login_required(login_url='login')
def Delete_Record(request,id):
    dataset = Dataset.objects.get(dataset_id = id)

    file_path = str(dataset.uploaded_file)
    final_path = os.path.join(settings.MEDIA_ROOT,file_path)
    os.remove(final_path)
    dataset.delete()
    

    return redirect('history')

@login_required(login_url='login')
def Analysis(request, id):
    dataset = Dataset.objects.get(dataset_id=id)
    plots = Plot.objects.filter(dataset=dataset)
    df = pd.read_csv(dataset.uploaded_file)
    notes = Note.objects.filter(user = request.user,dataset = dataset)
    row, col = df.shape
    head = df.head()
    info = pd.DataFrame({
        'Column': df.columns,
        'Non-Null Count': df.count(),
        'Data Type': df.dtypes
    })
    Nullval = pd.DataFrame({'Column': df.columns, 'Null Count': df.isnull().sum()})
    Nullval = Nullval[Nullval['Null Count'] > 0]
    desc = df.describe().reset_index()

    context = {
        'head': head,
        'info': info,
        'desc': desc,
        'Nullval': Nullval,
        'my_id':id,
        'title':dataset.dataset_name,
        'notes':notes,
        'plots':plots,
    }
    return render(request, 'analysis/dataAnalysis.html', context)



@login_required(login_url='login')
def mean_imputation(request,id):
    try:
        dataset = Dataset.objects.get(dataset_id=id)
        file_path = dataset.uploaded_file.path

        df = pd.read_csv(file_path)

        for column in df.columns:
            if df[column].dtype.kind in 'biufc': 
                if df[column].isnull().any():
                    mean_value = df[column].mean()
                    df[column].fillna(mean_value, inplace=True)
            else:
                df[column].fillna('NULL', inplace=True)

        df.to_csv(file_path, index=False)

        messages.success(request, "Mean imputation completed successfully for int and float datatype.")
    except Dataset.DoesNotExist:
        messages.error(request, "Dataset with the provided ID does not exist.")

    return redirect("data-analysis",id=id)


@login_required(login_url='login')
def median_imputation(request,id):

    dataset = Dataset.objects.get(dataset_id=id)
    file_path = dataset.uploaded_file.path

    df = pd.read_csv(file_path)

    for column in df.columns:
        if df[column].dtype.kind in 'biufc':  # Check if column data type is numeric
            if df[column].isnull().any():
                median_value = df[column].median()
                df[column].fillna(median_value, inplace=True)
        else:
            # For non-numeric (Object) columns, replace null values with 'NULL'
            df[column].fillna('NULL', inplace=True)

    # Save the modified DataFrame back to the CSV file in the database
    df.to_csv(file_path, index=False)
    messages.success(request, "Median imputation completed successfully for non-numeric datatype.")
    return redirect("data-analysis",id=id)

@login_required(login_url='login')
def mode_imputation(request,id):

    dataset = Dataset.objects.get(dataset_id=id)
    file_path = dataset.uploaded_file.path

    df = pd.read_csv(file_path)

    for column in df.columns:
        if df[column].dtype.kind not in 'biufc':  # Check if column data type is not numeric (i.e., Object)
            if df[column].isnull().any():
                mode_value = df[column].mode()[0]  # Mode may have multiple values, so we take the first one
                df[column].fillna(mode_value, inplace=True)
        else:
            # For numeric columns, replace null values with the median
            median_value = df[column].median()
            df[column].fillna(median_value, inplace=True)

    # Save the modified DataFrame back to the CSV file in the database
    df.to_csv(file_path, index=False)

    # Display a success message for mode imputation
    messages.success(request, "Mode imputation completed successfully for non-numeric datatype.")
    return redirect("data-analysis",id=id)


@login_required(login_url='login')
def DownloadDataset(request, id):
    dataset = Dataset.objects.get(dataset_id=id)
    file_path = dataset.uploaded_file.path

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/csv')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    else:
        return HttpResponse("File not found.", status=404)



@login_required(login_url='login')
def AddNote(request,id):
    if request.method == 'POST':
        dataset = Dataset.objects.get(dataset_id=id)
        note = request.POST.get('insight')
        heading = request.POST.get('heading')
        note = Note(user=request.user,dataset=dataset,note = note,heading=heading)
        note.save()    
        messages.success(request, "Your Insight Added succesfully!!!")
        return redirect("data-analysis",id=id)

    return redirect("data-analysis",id=id)


@login_required(login_url='login')
def DeleteNote(request,id):
    note = Note.objects.get(note_id = id)
    dataset = note.dataset
    newid = dataset.dataset_id
    note.delete()
    messages.success(request, "Your Insight Deleted succesfully!!!")
    return redirect("data-analysis",id=newid)




def generate_analysis_report(request, id):
    dataset = Dataset.objects.get(dataset_id=id)
    plots = Plot.objects.filter(dataset=dataset)
    df = pd.read_csv(dataset.uploaded_file.path)
    notes = Note.objects.filter(user=request.user, dataset=dataset)
    row, col = df.shape
    head = df.head()
    info = pd.DataFrame({
        'Column': df.columns,
        'Non-Null Count': df.count(),
        'Data Type': df.dtypes
    })
    Nullval = pd.DataFrame({'Column': df.columns, 'Null Count': df.isnull().sum()})
    Nullval = Nullval[Nullval['Null Count'] > 0]
    desc = df.describe().reset_index()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="analysis_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    story = []

    # Title
    styles = getSampleStyleSheet()
    story.append(Paragraph("Analysis Report", styles['Title']))

    # Add dataset title
    story.append(Paragraph(dataset.dataset_name, styles['Heading1']))

    # Add data summary tables
    head_table = Table(head.values.tolist())
    info_table = Table(info.values.tolist())
    desc_table = Table(desc.values.tolist())
    story.append(head_table)
    story.append(info_table)
    story.append(desc_table)

    # Add notes
    story.append(Paragraph("Notes:", styles['Heading2']))
    for note in notes:
        story.append(Paragraph(note.note, styles['Normal']))

    # Add plots
    story.append(Paragraph("Plots:", styles['Heading2']))
    for plot in plots:
        img_data = plot.data.get('plot_image', None)
        if img_data:
            img = Image(BytesIO(base64.b64decode(img_data)))
            img.drawHeight = 300
            img.drawWidth = 500
            story.append(img)

    doc.build(story)
    
    return response