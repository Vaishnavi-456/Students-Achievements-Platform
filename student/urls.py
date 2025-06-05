
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('student/', views.home, name='home'),
    path('student/login', views.login, name='login'),
    path('student/logout', views.logout, name='logout'),
    path('student/register', views.register, name='register'),
    path('student/edit_profile', views.edit_profile, name='edit_profile'),
    path('student/profile', views.profile, name='profile'),
    path('student/change_password', views.change_password, name='change_password'),
    
    path('student/view_events', views.view_events, name='view_events'),
    path('student/event_details/<int:event_id>', views.event_details, name='event_details'),
    path('student/register_event/<int:event_id>', views.register_event, name='register_event'),
    
    
    path('student/view_workshops', views.view_workshops, name='view_workshops'),
    path('student/workshop_details/<int:workshop_id>', views.workshop_details, name='workshop_details'),
    path('student/register_workshop/<int:workshop_id>', views.register_workshop, name='register_workshop'),
    
    path('student/view_compititions', views.view_compititions, name='view_compititions'),
    path('student/compitition_details/<int:compitition_id>', views.compitition_details, name='compitition_details'),
    path('student/register_compitition/<int:compitition_id>', views.register_compitition, name='register_compitition'),
    
    path('student/view_certificates', views.view_certificates, name='view_certificates'),
    path('student/certificate_details/<str:certificate_id>', views.certificate_details, name='certificate_details'),
    path('student/download_certificate/<str:certificate_id>', views.download_certificate, name='download_certificate'),
    # In urls.py
    path('certificate/download/<str:certificate_id>/', views.download_certificate, name='download_certificate'),
]
