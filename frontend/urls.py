from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

app_name = 'frontend'
urlpatterns = [
    path('', views.LoginView.as_view() , name='login'),
    path('signup/', views.SignupView.as_view() , name='signup'),
    path('biorhythm/<user_id>', views.BiorhythmView.as_view() , name='biorhythm'),
    path('biorhythm/friend/<user_id>', views.FriendBiorhythm.as_view() , name='friendbiorhythm'),
    path('contacts/<user_id>', views.eventList , name='contacts'),
    path('events/<user_id>', views.schedulerView , name='events'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
