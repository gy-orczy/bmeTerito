from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('generate-essay/', views.generate_essay, name='generate-essay')
]