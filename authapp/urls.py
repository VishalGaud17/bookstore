from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', LoginView.as_view(template_name='authapp/login.html'), name='login'),
] 
