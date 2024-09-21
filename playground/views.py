from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer

def say_hello(request):
    # customer = Customer.objects.filter(membership=Customer.MEMBERSHIP_BRONZE).order_by('first_name')[5:15]
    customer = Customer.objects.values('first_name', 'last_name', 'membership').order_by('first_name')[5:15]
    
    
    return render(request, 'hello.html', {'name': 'Mosh', 'customers': customer})