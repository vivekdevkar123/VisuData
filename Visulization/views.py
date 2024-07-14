from django.shortcuts import render,redirect
import pandas as pd
from EDA.models import Dataset
import json
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import base64
from .models import Plot
from django.contrib import messages
import seaborn as sns


def Visulization_Home(request, id):
    try:
        # Check if a plot image is stored in the session
        plot_image = request.session.get('plot_image', None)
        
        if plot_image:
            context = {'plot_image': plot_image}
        else:
            context = {}  # Initialize an empty context if no plot image
        
        dataset = Dataset.objects.get(dataset_id=id)
        df = pd.read_csv(dataset.uploaded_file.path)
        columns = df.select_dtypes(include=['number'])
        column_names = columns.columns.tolist()[1:]

        context.update({
            'title': dataset.dataset_name,
            'my_id': dataset.dataset_id,
            'column_names': column_names,
        })

        return render(request, 'visulization/index.html', context)
    except:
        messages.error(request, "Error occured")


def scatter_plot(request, id):
    try:
        dataset = Dataset.objects.get(dataset_id=id)
        df = pd.read_csv(dataset.uploaded_file.path)
        column_names = df.columns.tolist()
        
        if request.method == 'POST':
            heading = request.POST.get('scatter-plot-heading')
            x_axis_label = request.POST.get('x-axis-label')
            y_axis_label = request.POST.get('y-axis-label')
            x_axis_column = request.POST.get('x_axis')
            y_axis_column = request.POST.get('y_axis')
            
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x_axis_column], df[y_axis_column])
            plt.title(heading)
            plt.xlabel(x_axis_label)
            plt.ylabel(y_axis_label)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            plot_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Save the plot_image to the session to pass it to the home view
            request.session['plot_image'] = plot_image
            
            return redirect('Visulization-Home',id=id)
        
        context = {
            'title': dataset.dataset_name,
            'my_id': dataset.dataset_id,
            'column_names': column_names,
        }
        return render(request, 'visulization/index.html', context)
    except:
        messages.error(request, "Failed to draw scatter plot")


def line_plot(request, id):
    try:
        dataset = Dataset.objects.get(dataset_id=id)
        df = pd.read_csv(dataset.uploaded_file.path)
        column_names = df.columns.tolist()
        
        if request.method == 'POST':
            heading = request.POST.get('line-plot-heading')
            y_axis_label = request.POST.get('y-axis-label')
            y_axis_column = request.POST.get('y_axis')
            line_color = request.POST.get('line_color')
            
            plt.figure(figsize=(10, 6))
            
            # Use Seaborn's line plot
            sns.lineplot(data=df, x=df.index, y=y_axis_column, color=line_color)
            
            plt.title(heading)
            plt.ylabel(y_axis_label)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            plot_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Save the plot_image to the session to pass it to the home view
            request.session['plot_image'] = plot_image
            
            return redirect('Visulization-Home', id=id)
        
        context = {
            'title': dataset.dataset_name,
            'my_id': dataset.dataset_id,
            'column_names': column_names,
        }
        return render(request, 'visulization/index.html', context)

    except:
        messages.error(request, "fail to draw line plot")




def bar_chart(request, id):
    try:
        dataset = Dataset.objects.get(dataset_id=id)
        df = pd.read_csv(dataset.uploaded_file.path)
        column_names = df.columns.tolist()
        
        if request.method == 'POST':
            heading = request.POST.get('bar-chart-heading')
            x_axis_label = request.POST.get('x-axis-label')
            y_axis_label = request.POST.get('y-axis-label')
            x_axis_column = request.POST.get('x_axis')
            y_axis_column = request.POST.get('y_axis')
            bar_color = request.POST.get('bar_color')
            
            plt.figure(figsize=(10, 6))
            
            # Create a bar chart using Matplotlib
            plt.bar(df[x_axis_column], df[y_axis_column], color=bar_color)
            plt.title(heading)
            plt.xlabel(x_axis_label)
            plt.ylabel(y_axis_label)
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            plot_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Save the plot_image to the session to pass it to the home view
            request.session['plot_image'] = plot_image
            
            return redirect('Visulization-Home', id=id)
        
        context = {
            'title': dataset.dataset_name,
            'my_id': dataset.dataset_id,
            'column_names': column_names,
        }
        return render(request, 'visulization/index.html', context)

    except:
        messages.error(request, "failed to draw bar chart")


def histogram(request, id):
    try:
        dataset = Dataset.objects.get(dataset_id=id)
        df = pd.read_csv(dataset.uploaded_file.path)
        column_names = df.columns.tolist()
        
        if request.method == 'POST':
            heading = request.POST.get('histogram-heading')
            x_axis_label = request.POST.get('x-axis-label')
            x_axis_column = request.POST.get('x_axis')
            histogram_color = request.POST.get('histogram_color')
            
            plt.figure(figsize=(10, 6))
            
            # Create a histogram using Matplotlib
            plt.hist(df[x_axis_column], bins='auto', color=histogram_color)
            plt.title(heading)
            plt.xlabel(x_axis_label)
            plt.ylabel('Frequency')
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            plot_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Save the plot_image to the session to pass it to the home view
            request.session['plot_image'] = plot_image
            
            return redirect('Visulization-Home', id=id)
    
        context = {
            'title': dataset.dataset_name,
            'my_id': dataset.dataset_id,
            'column_names': column_names,
        }
        return render(request, 'visulization/index.html', context)

    except:
        messages.error(request, "failed to draw histogram")



def Save_Plot(request, id):
    try:
        plot_image = request.session.get('plot_image', None)
        dataset = Dataset.objects.get(dataset_id=id)
        if plot_image:
            plot = Plot(dataset=dataset, data={'plot_image': plot_image})
            plot.save()
            messages.success(request, "Plot saved successfully!!!")
            del request.session['plot_image']
            
        return redirect('Visulization-Home', id=id)
    except:
        messages.error(request, "Chart not saved please try again")

def Delete_Plot(request, id):
    try:
        del request.session['plot_image']
        messages.warning(request, "Plot deleted successfully!!!")
        return redirect('Visulization-Home', id=id)
    except:
        messages.error(request, "fail to delete plot")

def Delete_Plot_Img(request, id):
    try:
        img = Plot.objects.get(plot_id = id)
        img.delete()
        messages.warning(request, "Plot deleted successfully!!!")
        id = img.dataset.dataset_id
        return redirect('data-analysis', id=id)
    except:
        messages.error(request, "failed to delete plot image")