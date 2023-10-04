from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='incomes-index'),
    path('add-income/',views.add_income,name='add-income'),
    path('edit-income/<int:pk>',views.edit_income,name='edit-income'),
    path('income_delete/<int:pk>',views.income_delete,name='delete-income'),
    path('search_incomes/',csrf_exempt(views.search_incomes),name='search_incomes'),
    path('incomes_summary/',csrf_exempt(views.category_income_summary),name='incomes_summary'),
    path('incomes_summary_page/',csrf_exempt(views.category_income_summary_page),name='incomes_summary_page'),
    path('export_income_to_pdf/', views.advanced_pdf_view, name='export_income_to_pdf'),
] 
