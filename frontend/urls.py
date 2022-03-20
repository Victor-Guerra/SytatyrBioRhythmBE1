from django.urls import path
from . import views

app_name = "frontend"
urlpatterns = [
    path('', views.loginView , name='login'),
    path('signup/', views.signupView , name='signup'),
    path('biorhythm/<user_id>', views.biorhythmView , name='biorhythm'),
    path('events/<user_id>', views.eventList , name='events'),
] 
