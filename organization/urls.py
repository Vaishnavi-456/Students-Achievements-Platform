from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),

    path('add_event/', views.add_event, name='add_event'),
    path('view_events/', views.view_events, name='view_events'),
    path('generate_event_certificate/<int:event_id>', views.generate_event_certificate, name='generate_event_certificate'),
    
    path('add_workshop/', views.add_workshop, name='add_workshop'),
    path('view_workshops/', views.view_workshops, name='view_workshops'),
    path('generate_workshop_certificate/<int:workshop_id>/', views.generate_workshop_certificate, name='generate_workshop_certificate'),
    path('view_workshop_certificate/<int:workshop_id>/', views.view_workshop_certificate, name='view_workshop_certificate'),
    
    path('add_compitition/', views.add_compitition, name='add_compitition'),
    path('view_compititions/', views.view_compititions, name='view_compititions'),
    path('generate_compitition_certificate/<int:compitition_id>', views.generate_compitition_certificate, name='generate_compitition_certificate'),
    
    path('verify_certificate/', views.verify_certificate, name='verify_certificate'),
    
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('view_event_participants/<int:event_id>/', views.view_event_participants, name='view_event_participants'),
    
    path('edit_compitition/<int:compitition_id>/', views.edit_compitition, name='edit_compitition'),
    path('delete_compitition/<int:compitition_id>/', views.delete_compitition, name='delete_compitition'),
    path('view_compitition_participants/<int:compitition_id>/', views.view_compitition_participants, name='view_compitition_participants'),
    
    
    path('edit_workshop/<int:workshop_id>/', views.edit_workshop, name='edit_workshop'),    
    path('delete_workshop/<int:workshop_id>/', views.delete_workshop, name='delete_workshop'),
    path('view_workshop_participants/<int:workshop_id>/', views.view_workshop_participants, name='view_workshop_participants'),
    
    # path('view_certificate/<int:certificate_id>/', views.view_certificate, name='view_certificate'),
]
