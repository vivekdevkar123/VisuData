from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Dataset
from django.http import HttpResponse
import pandas as pd
import numpy as np
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
            if file_extension not in ['csv', 'xlsx']:
                return HttpResponse("Invalid file format. Only CSV and Excel files are allowed.")

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

    dataset.delete()

    return redirect('history')

@login_required(login_url='login')
def Analysis(request,id):
    dataset = Dataset.objects.get(dataset_id = id)

    df = pd.read_csv(dataset.uploaded_file)
    row, col = df.shape 

    head = df.head()

    context = {
        'head':head,
    }
    return render(request,'analysis/dataAnalysis.html',context)