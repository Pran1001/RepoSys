from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('profile/', views.profile, name='profile'),
    path('education/', views.education, name='education'),
    path('certificates/', views.certificates, name='certificates'),
    path('report/', views.report, name='report'),

]