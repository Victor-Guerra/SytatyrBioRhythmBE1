from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView , name='login'),
    path('signup/', views.signupView , name='signup'),
    path('biorhythm/<int:user_id>', views.biorhythmView , name='biorhythm'),
] 
