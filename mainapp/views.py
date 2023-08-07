from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ContactU
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'basic/index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('desc')

        contactus = ContactU(name=name,email=email,phone=phone,description=description)
        contactus.save()
        messages.success(request, "Thank You For Your Feedback!!!")

        return redirect('home')
    
    return render(request,'basic/contact.html')

def about(request):
    return render(request,'basic/about.html')

def search(request):
    return render(request,'basic/search.html')