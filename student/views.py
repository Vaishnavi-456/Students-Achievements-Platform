from django.shortcuts import render
from organization.models import Events, Workshops, Compititions, Event_Participations, Workshop_Participations, Compitition_Participations
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime,date
from django.db.models import Count
from django.contrib.auth.hashers import make_password, check_password
from .models import Student
from functools import wraps
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
import os
import tempfile
from django.conf import settings

# Create a decorator for login required checks
def student_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('student_id'):
            messages.error(request, 'Please login to continue', extra_tags='alert alert-danger')
            return redirect('student:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.

def home(request):
    events = Events.objects.all().order_by('-date')[:5]  # Show 6 most recent events
    workshops = Workshops.objects.all().order_by('-date')[:5]
    compititions = Compititions.objects.all().order_by('-date')[:5]
    return render(request, 'student/home.html', {'events': events, 'workshops': workshops, 'compititions': compititions, 'today':date.today() })

@student_login_required
def profile(request):
    student = Student.objects.get(email=request.session['student_id'])
    return render(request, 'student/profile.html', {'student': student})

@student_login_required
def edit_profile(request):
    student = Student.objects.get(email=request.session['student_id'])
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.college = request.POST['college']
        student.phone = request.POST['phone']
        student.address = request.POST['address']
        student.city = request.POST['city']
        student.state = request.POST['state']
        student.zip_code = request.POST['zip_code']
        student.country = request.POST['country']
        student.save()
        messages.success(request, 'Profile updated successfully', extra_tags='alert alert-success')
        return redirect('student:profile')
    return render(request, 'student/edit_profile.html', {'student': student})

@student_login_required
def change_password(request):
    if request.method == 'POST':
        student = Student.objects.get(email=request.session['student_id'])
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if not check_password(old_password, student.password):
            messages.error(request, 'Invalid old password', extra_tags='alert alert-danger')
            return render(request, 'student/change_password.html')
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match', extra_tags='alert alert-danger')
            return render(request, 'student/change_password.html')
        student.password = make_password(new_password)
        student.save()
        messages.success(request, 'Password updated successfully', extra_tags='alert alert-success')
        return redirect('student:profile')
    return render(request, 'student/change_password.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Student.objects.filter(email=email).exists():
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                request.session['student_id'] = student.email
                request.session['student_first_name'] = student.first_name 
                request.session['student_last_name'] = student.last_name 
                
                return redirect('student:home')
            else:
                messages.error(request, 'Invalid Password', extra_tags='alert alert-danger')
                return render(request, 'student/login.html')
        else:
            messages.error(request, 'Invalid Email', extra_tags='alert alert-danger')
            return render(request, 'student/login.html')
    return render(request, 'student/login.html')

def logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully', extra_tags='alert alert-success')
    return redirect('student:login')
    
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists', extra_tags='alert alert-danger')
            return render(request, 'student/register.html')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match', extra_tags='alert alert-danger')
            return render(request, 'student/register.html')
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        college = request.POST['college']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        country = request.POST['country']
        
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            college=college,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country
        )
        
        if student:
            messages.success(request, 'Registration Successful', extra_tags='alert alert-success')
            return redirect('student:login')
        else:
            messages.error(request, 'Registration Failed', extra_tags='alert alert-danger')
            return redirect('student:register')
            
    return render(request, 'student/register.html')


def view_events(request):
    
    events = Events.objects.all()
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(name__icontains=search_query)
    # Handle filters
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'upcoming':
        events = events.filter(date__gte=datetime.now().date())
    elif filter_type == 'past':
        events = events.filter(date__lt=datetime.now().date())
    elif filter_type == 'popular':
        events = events.annotate(participant_count=Count('event_participations')).order_by('-participant_count')
    
    # Handle sorting
    sort_by = request.GET.get('sort', '-date')
    events = events.order_by(sort_by)

    context = {
        'events': events,
        'current_filter': filter_type,
        'search_query': search_query,
        'sort_by': sort_by,
        'today': datetime.now().date()
    }
    
    return render(request, 'student/view_events.html', context)
import random
import string
@student_login_required
def register_event(request, event_id):
    event = Events.objects.get(id=event_id)
    participation_id = 'E' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    
    if Event_Participations.objects.filter(event=event, student=Student.objects.get(email=request.session['student_id'])).exists():
        messages.error(request, 'Already Registered', extra_tags='alert alert-danger')
        return redirect('student:event_details', event_id=event_id)

    if Event_Participations.objects.create(event=event, student=Student.objects.get(email=request.session['student_id']), participation_id=participation_id).save() :
        messages.success('Registration Successful', extra_tags='alert alert-success')
        return redirect('event_details', event_id=event_id)
    else:
        #messages.error(request, 'Registration Failed', extra_tags='alert alert-danger')
        return redirect('student:event_details', event_id=event_id)
    pass

def event_details(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if "student_id" in request.session:
        is_registered = Event_Participations.objects.filter(
            event=event,
            
            student=Student.objects.get(email=request.session.get('student_id'))
        ).exists()

        context = {
            'event': event,
            'is_registered': is_registered
        }
    else:
        context = {
            'event': event,
            'is_registered': False
        }
    return render(request, 'student/event_details.html', context)


def view_workshops(request):
    workshops = Workshops.objects.all()
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        workshops = workshops.filter(name__icontains=search_query)
    # Handle filters
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'upcoming':
        workshops = workshops.filter(date__gte=datetime.now().date())
    elif filter_type == 'past':
        workshops = workshops.filter(date__lt=datetime.now().date())
    elif filter_type == 'popular':
        workshops = workshops.annotate(participant_count=Count('event_participations')).order_by('-participant_count')
    
    # Handle sorting
    sort_by = request.GET.get('sort', '-date')
    workshops = workshops.order_by(sort_by)

    context = {
        'workshops': workshops,
        'current_filter': filter_type,
        'search_query': search_query,
        'sort_by': sort_by,
        'today': datetime.now().date()
    }
    
    return render(request, 'student/view_workshops.html', context)

def workshop_details(request, workshop_id):
    workshop = get_object_or_404(Workshops, id=workshop_id)
    if "student_id" in request.session:
        is_registered = Workshop_Participations.objects.filter(
            workshop=workshop,
            student=Student.objects.get(email=request.session.get('student_id'))
        ).exists()
        
        context = {
            'workshop': workshop,
            'is_registered': is_registered
        }
    else:
        context = {
            'workshop': workshop,
            'is_registered': False
        }
    # Remove the extra nesting of context
    return render(request, 'student/workshop_details.html', context)

@student_login_required
def register_workshop(request, workshop_id):
    if request.method == 'POST':
        workshop = Workshops.objects.get(id=workshop_id)
        participation_id = 'W' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        
        if Workshop_Participations.objects.filter(workshop=workshop, student=Student.objects.get(email=request.session['student_id'])).exists():
            messages.error(request, 'Already Registered', extra_tags='alert alert-danger')
            return redirect('student:workshop_details', workshop_id=workshop_id)

        
        if Workshop_Participations.objects.create(workshop=workshop, student=Student.objects.get(email=request.session['student_id']), participation_id=participation_id).save() :
            messages.success('Registration Successful', extra_tags='alert alert-success')
            return redirect('workshop_details', workshop_id=workshop_id)
        else:
           # messages.error(request, 'Registration Failed', extra_tags='alert alert-danger')
            return redirect('student:workshop_details', workshop_id=workshop_id)
    pass

def view_compititions(request):
    compititions = Compititions.objects.all()
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        compititions = compititions.filter(name__icontains=search_query)
    # Handle filters
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'upcoming':
        compititions = compititions.filter(date__gte=datetime.now().date())
    elif filter_type == 'past':
        compititions = compititions.filter(date__lt=datetime.now().date())
    elif filter_type == 'popular':
        compititions = compititions.annotate(participant_count=Count('event_participations')).order_by('-participant_count')
    
    # Handle sorting
    sort_by = request.GET.get('sort', '-date')
    compititions = compititions.order_by(sort_by)

    context = {
        'compititions': compititions,
        'current_filter': filter_type,
        'search_query': search_query,
        'sort_by': sort_by,
        'today': datetime.now().date()
    }
    return render(request, 'student/view_compititions.html', context)

def compitition_details(request, compitition_id):
    compitition = Compititions.objects.get(id=compitition_id)
    if "student_id" in request.session:
        is_registered = Compitition_Participations.objects.filter(
            compitition=compitition,
            student=Student.objects.get(email=request.session.get('student_id'))
        ).exists()
        
        context = {
            'compitition': compitition,
            'is_registered': is_registered
        }
    else:
        context = {
            'compitition': compitition,
            'is_registered': False
        }
    return render(request, 'student/compitition_details.html', context)
  

@student_login_required
def register_compitition(request, compitition_id):
    compitition = Compititions.objects.get(id=compitition_id)
    participation_id = 'C' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    if Compitition_Participations.objects.filter(compitition=compitition, student=Student.objects.get(email=request.session['student_id'])).exists():
        messages.error(request, 'Already Registered', extra_tags='alert alert-danger')
        return redirect('student:compitition_details', compitition_id=compitition_id)
    
    if Compitition_Participations.objects.create(compitition=compitition, student=Student.objects.get(email=request.session['student_id']), participation_id=participation_id).save() :
        messages.success('Registration Successful', extra_tags='alert alert-success')
        return redirect('compitition_details', compitition_id=compitition_id)
    else:
        #messages.error(request, 'Registration Failed', extra_tags='alert alert-danger')
        return redirect('student:compitition_details', compitition_id=compitition_id)
    pass


def view_certificates(request):
    if request.session['student_id'] is None:
        return redirect('student:login')
    student = Student.objects.get(email=request.session['student_id'])
    event_certificates = Event_Participations.objects.filter(student=student)  
    workshop_certificates = Workshop_Participations.objects.filter(student=student)
    compitition_certificates = Compitition_Participations.objects.filter(student=student)
    
    certificates ={
        'events': event_certificates,
        'workshops': workshop_certificates,
        'competitions': compitition_certificates
    }
    return render(request, 'student/view_certificates.html', certificates)


def certificate_details(request, certificate_id):
    if certificate_id[0] == 'e' or certificate_id[0] == 'E':
        certificate = Event_Participations.objects.get(participation_id=certificate_id)
        return render(request, 'student/certificate.html', {'certificate': certificate, 'event_mode':1})
    elif certificate_id[0] == 'w' or certificate_id[0] == 'W':
        certificate = Workshop_Participations.objects.get(participation_id=certificate_id)
        return render(request, 'student/certificate.html', {'certificate': certificate, 'event_mode':2})
    elif certificate_id[0] == 'c' or certificate_id[0] == 'C':
        certificate = Compitition_Participations.objects.get(participation_id=certificate_id)
        return render(request, 'student/certificate.html', {'certificate': certificate, 'event_mode':3})


def download_certificate(request, certificate_id):
    """Generate and download a certificate as PDF"""
    if not request.session.get('student_id'):
        return redirect('student:login')
        
    student = Student.objects.get(email=request.session['student_id'])
    
    # Determine certificate type based on ID prefix
    if certificate_id[0] in ('e', 'E'):
        certificate = get_object_or_404(Event_Participations, participation_id=certificate_id)
        certificate_type = "Event"
        event_name = certificate.event.name
        organization_name = certificate.event.organization.name
        event_date = certificate.event.date
       
        
    elif certificate_id[0] in ('w', 'W'):
        certificate = get_object_or_404(Workshop_Participations, participation_id=certificate_id)
        certificate_type = "Workshop"
        event_name = certificate.workshop.name
        organization_name = certificate.workshop.organization.name
        event_date = certificate.workshop.date

        
    elif certificate_id[0] in ('c', 'C'):
        certificate = get_object_or_404(Compitition_Participations, participation_id=certificate_id)
        certificate_type = "Competition"
        event_name = certificate.compitition.name
        organization_name = certificate.compitition.organization.name
        event_date = certificate.compitition.date

    
    # Create context for certificate template
    context = {
        'student': student,
        'certificate_id': certificate_id,
        'certificate_type': certificate_type,
        'event_name': event_name,
        'organization_name': organization_name,
        'event_date': event_date,
        
    }
    
    # Render the template to a string
    html_string = render_to_string('student/certificate_pdf.html', context)
    
    # Create a filename with event name and certificate ID
    filename = f"{certificate_type}_{event_name.replace(' ', '_')}_{certificate_id}.pdf"
    
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        pdf_path = temp_file.name
    
    # PDF generation options
    options = {
        'page-size': 'Letter',
        'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
    }
    
    # try:
    # Remove weasyprint import from the top of the file
    import pdfkit
    
    # Set the path to the wkhtmltopdf executable
    # Check if we're on Windows
    if os.name == 'nt':
        # Look for wkhtmltopdf in several possible locations
        wkhtmltopdf_paths = [
            r'static\wkhtmltopdf.exe',
            os.path.join(settings.BASE_DIR, 'static', 'wkhtmltopdf.exe'),
            ]
        
        # Find the first path that exists
        wkhtmltopdf_path = None
        for path in wkhtmltopdf_paths:
            if os.path.exists(path):
                wkhtmltopdf_path = path
                break
        
        if wkhtmltopdf_path:
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            pdfkit.from_string(html_string, pdf_path, options=options, configuration=config)
        else:
            # If no path found, try without configuration (may work if in PATH)
            pdfkit.from_string(html_string, pdf_path, options=options)
    else:
        # For Linux/Mac, usually in PATH
        pdfkit.from_string(html_string, pdf_path, options=options)
    
    # Read the generated PDF
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Clean up the temporary file
    os.unlink(pdf_path)
    return response
    
    # except Exception as e:
    #     # Log the error
    #     print(f"PDFKit error: {e}")
        
    #     # Instead of trying WeasyPrint as fallback, show an error message
    #     messages.error(request, "Failed to generate certificate. Please try again later.", extra_tags='alert alert-danger')
        
    #     # Clean up temporary file if it exists
    #     if os.path.exists(pdf_path):
    #         os.unlink(pdf_path)
            
    return redirect('student:view_certificates')


