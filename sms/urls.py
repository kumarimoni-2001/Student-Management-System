from django.urls import path
from .views import user_login, register,view_results, home, user_logout,add_student,add_marks,calculate_result

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='logout'),
    path('results/', view_results, name='view_results'),
    path('add-student/', add_student, name='add_student'),
    path('add-marks/', add_marks, name='add_marks'), 
    path('calculate/', calculate_result, name='calculate_result'), 

    
]

