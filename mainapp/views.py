from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'basic/index.html')

def contact(request):
    return render(request,'basic/contact.html')

def about(request):
    return render(request,'basic/about.html')

def search(request):
    return render(request,'basic/search.html')