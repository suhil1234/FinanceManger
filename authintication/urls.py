from . import views
from django.urls import path
from django.contrib.auth import views as authViews
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',authViews.LogoutView.as_view(template_name='auth/logout.html'),name='logout'),
    path('validate_username/',csrf_exempt(views.validate_username),name='validate_username'),
    path('validate_email/',csrf_exempt(views.validate_mail),name='validate_email'),
    path('validate_pass/',csrf_exempt(views.validate_pass),name='validate_pass'),
    path('validate_repass/',csrf_exempt(views.check_password_match),name='validate_repass'),
] 
