from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-student/', views.add_student, name='add_student'),
    path('add-marks/', views.add_marks, name='add_marks'),
    path('results/', views.view_results, name='view_results'),  # Fixed: view_results not results
    path('calculate/', views.calculate_result, name='calculate_result'),
]
