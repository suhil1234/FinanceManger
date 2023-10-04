from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='index'),
    path('add-expense/',views.add_expense,name='add-expense'),
    path('edit-expense/<int:pk>',views.edit_expense,name='edit-expense'),
    path('expense_delete/<int:pk>',views.expense_delete,name='delete-expense'),
    path('search_expenses/',csrf_exempt(views.search_expenses),name='search_expenses'),
    path('expenses_summary/',csrf_exempt(views.category_expense_summary),name='expenses_summary'),
    path('expenses_summary_page/',csrf_exempt(views.category_expense_summary_page),name='expenses_summary_page'),
    path('export-to-pdf/', views.advanced_pdf_view, name='export_to_pdf'),
] 
