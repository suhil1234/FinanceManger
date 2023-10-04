from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='userpreference'),
    path('categories',views.categories,name='categories'),
    path('add-category/',views.add_category,name='add-category'),
    path('category_delete/<int:pk>',views.expense_delete,name='delete-category'),
] 
