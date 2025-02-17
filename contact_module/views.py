from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.

def contact_page(request):
    if request.method == 'POST':
        return redirect(reverse('index'))
    return render(request, 'contact_module/contact-us.html')
