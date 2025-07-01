from django.urls import path
from . import views
from .views import program_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('products/', views.products, name='products'),
    path('industries/', views.industries, name='industries'),
    path('faqs/', views.faqs, name='faqs'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('accord-group/', views.accord_group, name='accord_group'),
    path('contact/', views.contact, name='contact'),
    path('programs/<int:pk>/', program_detail, name='program_detail'),
    path('download-catalog/', views.download_catalog, name='download_catalog'),
] 