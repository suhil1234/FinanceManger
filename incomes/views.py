import json
import datetime
import locale
from userPreference.models import userPreference
from . import renderers
from django.http import Http404, JsonResponse,HttpResponse
from django.shortcuts import redirect, render
from .models import Income,Categories
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q,Sum
# Create your views here.
def index(request):
    incomes = Income.objects.all().filter(owner=request.user)
    preference = userPreference.objects.get(user=request.user)
    paginator = Paginator(incomes, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'page_obj':page_obj,
        'currency':preference.currency
    }
    return render(request,'incomes/index.html',context)

def add_income(request):
    categories = Categories.objects.filter(user=request.user)
    context ={
        'categories' : categories
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = Categories.objects.get(id=request.POST['category'])
        date = request.POST['date']
        context={'categories':categories,
                 'data': request.POST,
                 'cat':category}
        if not amount or not amount.isdigit():
            messages.error(request,'you should put an amount and should be numbers')
            return render(request,'incomes/add-income.html',context)
        if not date:
            messages.error(request,'you should choose a date')
            return render(request,'incomes/add-income.html',context)        
        income = Income.objects.create(owner = request.user,amount= amount,
                                         description=description, category=category,date=date)
        income.save()
        return redirect('incomes-index')      
    if not categories:
        messages.info(request,'Please add some categories first')
            
    return render(request,'incomes/add-income.html',context)

def edit_income(request,pk):
    categories = Categories.objects.filter(user=request.user)
    income = Income.objects.get(pk=pk)
    category = Categories.objects.get(id=income.category_id)
    context ={
        'categories' : categories,
        'income': income,
        'pk':pk,
        'cat': category
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = Categories.objects.get(id=request.POST['category'])
        date = request.POST['date']
        context={'categories':categories,
                 'income': request.POST,
                 'cat':category,
                 'pk':pk,
                 'data':income}
        if not amount or not amount.isdigit():
            messages.error(request,'you should put an amount and should be numbers')
            return render(request,'incomes/edit-income.html',context)
        if not date:
            messages.error(request,'you should choose a date')
            return render(request,'incomes/edit-income.html',context)        
        income.amount=amount
        income.description=description
        income.category=category
        income.date=date
        income.save()
        return redirect('incomes-index')        
    return render(request,'incomes/edit-income.html',context)

def income_delete(request,pk):
    income = Income.objects.get(pk=pk)
    context ={'pk':income.id}
    if request.method =='POST':
        income.delete()
        return redirect('incomes-index') 
    return render(request,'incomes/delete-income.html',context)

def search_incomes(request):
    if request.method =='POST':
        categories = Categories.objects.filter(user=request.user)
        query = json.loads(request.body).get('search')
        if query:
            results = Income.objects.filter(
            Q(amount__icontains=query,owner=request.user) |
            Q(category__name__icontains=query,owner=request.user) |
            Q(date__icontains=query,owner=request.user) |
            Q(description__icontains=query,owner=request.user)
        )
            data=[]
            for income in results:
                income_data = {
                    'id': income.id,
                    'amount': income.amount,
                    'description': income.description,
                    'date': income.date,
                    'category': income.category.name  # Include category name
                }
                data.append(income_data)
            print (data)
        return JsonResponse(data,safe=False)

def category_income_summary(request):
    category_incomes = Income.objects.filter(owner=request.user).values('category__name').annotate(total_amount=Sum('amount'))
    category_summary = {}
    for category_income in category_incomes:
        category_name = category_income['category__name']
        total_amount = category_income['total_amount']
        category_summary[category_name] = total_amount

    print(category_summary)
    return JsonResponse(category_summary)

def category_income_summary_page(request):
    return render(request,'incomes/incomes-summary.html')

def advanced_pdf_view(request):
    locale.setlocale(locale.LC_ALL, "")
    incomes = Income.objects.filter(owner=request.user)
    context = {
       'incomes': incomes,
    }
    response = renderers.render_to_pdf("incomes/incomes_pdf.html", context)
    if response.status_code == 404:
        raise Http404("Invoice not found")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"incomes_{current_date}.pdf"
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response
