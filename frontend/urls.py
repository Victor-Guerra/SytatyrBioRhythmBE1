from django.urls import path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.loginView , name='login'),
    path('signup/', views.signupView , name='signup'),
    path('biorhythm/<int:user_id>', views.biorhythmView , name='biorhythm'),
    path('contacts/<int:user_id>', views.eventList , name='contacts'),
    path('events/<int:user_id>', views.schedulerView , name='events'),
] 
