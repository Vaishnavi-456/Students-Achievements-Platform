from django.contrib import admin
from django.urls import path, include
import organization, student
from django.shortcuts import redirect

def home(request):
    return redirect('student:home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('organization/', include(('organization.urls', 'organization'), namespace='organization')),
    path('', include(('student.urls', 'student'), namespace='student')),
    # path('', home, name='home'),
    
]

