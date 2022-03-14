from django.urls import path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView , name='login'),
    path('signup/', views.signupView , name='signup'),
    path('biorhythm/<user_id>', views.BiorhythmView.as_view() , name='biorhythm'),
    path('contacts/<user_id>', views.eventList , name='contacts'),
    path('events/<user_id>', views.schedulerView , name='events'),
] 
