from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView , name='login'),
    path('signup/', views.signupView , name='signup'),
    path('biorhythm/', views.biorhythmView , name='biorhythm'),
] 
