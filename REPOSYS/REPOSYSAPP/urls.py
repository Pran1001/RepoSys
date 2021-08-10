from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('about/', views.about, name='about'),
    path('forget/', views.forget, name='forget'),
    path('profile/', views.profile, name='profile'),
    path('report/', views.report, name='report'),
]