from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('forget/', views.forget, name='forget'),
    path('profile/', views.profile, name='profile'),
    path('education/', views.education, name='education'),
    path('certificates/', views.certificates, name='certificates'),
    path('report/', views.report, name='report'),
]