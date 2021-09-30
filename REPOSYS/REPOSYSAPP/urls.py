from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('contactus/', views.contact, name='contactus'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('profile/', views.profile, name='profile'),
    path('education/', views.education, name='education'),
    path('certificates/', views.certificates, name='certificates'),
    path('report/', views.report, name='report'),
    path('generate_full_report', views.generate_full_report),
    path('generate_filter_report', views.generate_filter_report, name='generate_filter_report'),
    path('contactus_done/', views.contactus_done, name='contactus_done'),

]
