import json
from pathlib import Path
from django.shortcuts import redirect, render

from expenses.models import Expense
from .models import Categories, userPreference
from django.contrib import messages

# Create your views here.
def index(request):
    preference = userPreference.objects.get(user=request.user)
    current_currency= preference.currency
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_file =  (BASE_DIR/ 'currencies.json')
    with open(data_file) as file:
        data = json.load(file)
    if request.method == 'GET':
        context = {'data': data,'current':current_currency}
        return render(request,'userPreference/index.html',context)
    if request.method == 'POST':
        curr = request.POST['currency']
        preference.currency = curr
        preference.save()
        context = {'data': data,'current':curr}
        messages.success(request, 'current currency changed successfuly')
        return render(request, 'userPreference/index.html',context )
    
def categories(request):
    categories = Categories.objects.all().filter(user=request.user)
    context ={
        'categories':categories
    }
    return render(request,'userPreference/categories.html',context)

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        context={'name':name}
        if not name or name.isdigit():
            messages.error(request,'you should put a name and it should be String')
            return render(request,'userPreference/add-category.html',context)
        category = Categories.objects.create(user = request.user,name= name)
        category.save()
        return redirect('categories')        
    return render(request,'userPreference/add-category.html')
    
def expense_delete(request,pk):
    category = Categories.objects.get(pk=pk)
    context ={'pk':category.id}
    if request.method =='POST':
        category.delete()
        return redirect('categories') 
    return render(request,'userPreference/delete-category.html',context)