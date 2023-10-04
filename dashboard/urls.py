from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='main-index'),
    path('dashboard_summary/',csrf_exempt(views.summary),name='dashboard_summary'),
] 
