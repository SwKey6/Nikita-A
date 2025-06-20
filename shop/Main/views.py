from django.shortcuts import render, redirect

def Main(request):
    return render(request, 'Main/index.html')

def About(request):
    return render(request, 'Main/about.html')

def Contacts(request):
    return render(request, 'Main/contacts.html')

def Services(request):
    return render(request, 'Main/services.html')

def Staff(request):
    return render(request, 'Main/staff.html')

def Portfolio(request):
    return render(request, 'Main/portfolio.html')