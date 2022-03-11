from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView , name='login'),
    path('signup/', views.signupView , name='signup'),
    path('biorhythm/', views.biorhythmView , name='biorhythm'),
] 
