from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'frontend'
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('biorhythm/<user_id>', views.BiorhythmView.as_view(), name='biorhythm'),
    path('contacts/<user_id>', views.FriendList.as_view(), name='contacts'),
    path('events/<user_id>', views.EventList.as_view(), name='events'),
    path('updateDetails/', views.updateUserDetails, name='updateUserDetails'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
