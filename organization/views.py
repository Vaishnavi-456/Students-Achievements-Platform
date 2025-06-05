from django.shortcuts import render, redirect
from .models import Workshops, Events, Compititions, Organizations, Workshop_Participations, Event_Participations, Compitition_Participations
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
# from django.utils import timezone
import datetime
# Create your views here.
def home(request):
    organization = Organizations.objects.get(email=request.session['organization_email'])
    events = Events.objects.filter(organization= organization)
    event_count = events.count()
    
    workshops = Workshops.objects.filter(organization=organization)
    workshop_count = workshops.count()
    
    
    compititions = Compititions.objects.filter(organization=organization)
    compitition_count = compititions.count()
    
    total_participants = 0
    
    if events:
        for event in events:
            total_participants += event.registration_count
    if workshops: 
        for workshop in workshops:
            total_participants += workshop.registration_count
    if compititions:
        for compitition in compititions:
            total_participants += compitition.registration_count
    
    
    
    return render(request, 'organization/home.html', {'event_count':event_count, 'workshop_count':workshop_count, 'compitition_count':compitition_count, 'total_participants':total_participants})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not Organizations.objects.filter(email=email).exists():
            messages.error(request, 'Invalid Email or Password')
            return redirect('organization:login')
        organization = Organizations.objects.get(email=email)
        if check_password(password, organization.password):
            request.session['organization_email'] = organization.email
            request.session['organization_name'] = organization.name
            
            return redirect('organization:home')
        messages.error(request, 'Invalid Email or Password')
        return redirct('organization:login')
    return render(request, 'organization/login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Organizations.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists')
            return render(request, 'organization/register.html')
        
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        website = request.POST.get('website')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            data = {'name':name, 'email':email, 'phone':phone, 'address':address, 'city':city, 'state':state, 'zip_code':zip_code, 'country':country, 'website':website}
            messages.error(request, 'Password and Confirm Password does not match')
            return render(request, 'organization/register.html',{'message':'Password and Confirm Password does not match','data':data})
        
        organization = Organizations(name=name, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code, country=country, website=website, password=make_password(password))
        organization.save()
        messages.success(request, 'Organization Registered Successfully')
        return redirect('organization:login')
        return render(request, 'organization/login.html',{'message':'Organization Registered Successfully'})
    return render(request, 'organization/register.html')

def logout(request):
    request.session.flush()
    messages.success(request, 'Logged Out Successfully')    
    return render(request, 'organization/login.html')


def profile(request):
    organization = Organizations.objects.get(email=request.session['organization_email'])
    return render(request, 'organization/profile.html',{'organization':organization})

def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        website = request.POST.get('website')
        organization = Organizations.objects.get(email=request.session['organization_email'])
        organization.name = name
        organization.phone = phone
        organization.address = address
        organization.city = city
        organization.state = state
        organization.zip_code = zip_code
        organization.country = country
        organization.website = website
        organization.save()
        return render(request, 'organization/profile.html',{'organization':organization,'message':'Profile Updated Successfully'})
    organization = Organizations.objects.get(email=request.session['organization_email'])
    return render(request, 'organization/edit_profile.html',{'organization':organization})

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        organization = Organizations.objects.get(email=request.session['organization_email'])
        if check_password(old_password, organization.password):
            if new_password == confirm_password:
                organization.password = make_password(new_password)
                organization.save()
                messages.success(request, 'Password Changed Successfully')
                return render(request, 'organization/profile.html',{'organization':organization})
            messages.error(request, 'New Password and Confirm Password does not match')
            return render(request, 'organization/change_password.html')
        messages.error(request, 'Old Password is Incorrect')
        return render(request, 'organization/change_password.html')
    return render(request, 'organization/change_password.html')


def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        print(name, description, date, time, location)
        organization = Organizations.objects.get(email=request.session['organization_email'])
        event = Events(name=name, description=description, date=date, time=time, location=location, organization=organization)
        event.save()
        messages.success(request, 'Event Added Successfully')
        return redirect('organization:view_events')
    return render(request, 'organization/add_event.html')

def view_events(request):
    events = Events.objects.filter(organization=Organizations.objects.get(email=request.session['organization_email']))
    return render(request, 'organization/view_events.html', {'events':events})

def generate_event_certificate(request, event_id):
    event = Events.objects.get(id=event_id)
    if event.date < datetime.date.today():
        event.certificate_generated = True
        event.save()
        
        messages.success(request, 'Certificate Generated Successfully')
        return redirect('organization:view_events')
    messages.error(request, f'Event {event.name} is not completed')
    return redirect('organization:view_events')


def add_workshop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
       
        organization = Organizations.objects.get(email=request.session['organization_email'])
        workshop = Workshops(name=name, description=description, date=date, time=time, location=location, organization=organization)
        workshop.save()
        messages.success(request, 'Workshop Added Successfully')
        return redirect('organization:view_workshops')
    return render(request, 'organization/add_workshop.html')


def view_workshops(request):
    workshops = Workshops.objects.filter(organization=Organizations.objects.get(email=request.session['organization_email']))
    return render(request, 'organization/view_workshops.html',{'workshops':workshops})

def generate_workshop_certificate(request, workshop_id):
    workshop = Workshops.objects.get(id=workshop_id)
    if workshop.date < datetime.date.today():
        workshop.certificate_generated = True
        workshop.save()
        
        messages.success(request, 'Certificate Generated Successfully')
        return redirect('organization:view_workshops')
    messages.error(request, f'workshop {workshop.name} is not completed')
    return redirect('organization:view_workshops')

def view_workshop_certificate(request, workshop_id):
    workshop = Workshops.objects.get(id=workshop_id)
    if workshop.certificate_generated:
        participants = Workshop_Participations.objects.filter(workshop=workshop)
        return render(request, 'organization/view_workshop_certificate.html', 
                     {'workshop': workshop, 'participants': participants})
    
    messages.error(request, f'Certificate not generated for workshop {workshop.name}')
    return redirect('organization:view_workshops')

def add_compitition(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
       
        organization = Organizations.objects.get(email=request.session['organization_email'])
        compitition = Compititions(name=name, description=description, date=date, time=time, location=location, organization=organization)
        compitition.save()
        messages.success(request, 'compitition Added Successfully')
        return redirect('organization:view_compititions')
    return render(request, 'organization/add_compitition.html')

def view_compititions(request):
    compititions = Compititions.objects.filter(organization=Organizations.objects.get(email=request.session['organization_email']))
    return render(request, 'organization/view_compititions.html',{'compititions':compititions})

def generate_compitition_certificate(request, compitition_id):
    compitition = Compititions.objects.get(id=compitition_id)
    if compitition.date < datetime.date.today():
        compitition.certificate_generated = True
        compitition.save()
        
        messages.success(request, 'Certificate Generated Successfully')
        return redirect('organization:view_compititions')
    messages.error(request, f'compitition {compitition.name} is not completed')
    return redirect('organization:view_compititions')


def verify_certificate(request):
    if request.method == 'POST':
        credential = request.POST.get('credential')
        if credential.startswith('E' or 'e'):
            event_mode = 1
            certificate = Event_Participations.objects.get(participation_id=credential)
            if certificate:
                print(certificate)
                return render(request, 'organization/certificate.html',{'certificate':certificate, 'event_mode':event_mode})
        
        elif credential.startswith('W' or 'w'):
            event_mode = 2
            certificate = Workshop_Participations.objects.get(participation_id=credential)
            if certificate:
                return render(request, 'organization/certificate.html',{'certificate':certificate, 'event_mode':event_mode})

        elif credential.startswith('C' or 'c'):
            event_mode = 3
            certificate = Compitition_Participations.objects.get(participation_id=credential)
            if certificate:
                return render(request, 'organization/certificate.html',{'certificate':certificate, 'event_mode':event_mode})
        
        messages.error(request, 'Invalid Credential')
        return render(request, 'organization/verify_certificate.html')
    return render(request, 'organization/verify_certificate.html')



def edit_event(request, event_id):
    event = Events.objects.get(id=event_id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.location = request.POST.get('location')
        event.save()
        messages.success(request, 'Event Updated Successfully')
        return redirect('organization:view_events')
    return render(request, 'organization/edit_event.html',{'event':event})

def delete_event(request, event_id):
    if Events.objects.get(id=event_id).delete():
        messages.success(request, 'Event Deleted Successfully')
        return redirect('organization:view_events')
    messages.error(request, 'Event Not Deleted')
    return redirect('organization:view_events')

def edit_compitition(request, compitition_id):
    compitition = Compititions.objects.get(id=compitition_id)
    if request.method == 'POST':
        compitition.name = request.POST.get('name')
        compitition.description = request.POST.get('description')
        compitition.date = request.POST.get('date')
        compitition.time = request.POST.get('time')
        compitition.location = request.POST.get('location')
        compitition.save()
        messages.success(request, 'compitition Updated Successfully')
        return redirect('organization:view_compititions')
    return render(request, 'organization/edit_compitition.html',{'compitition':compitition})
    
def delete_compitition(request, compitition_id):
    if Compititions.objects.get(id=compitition_id).delete():
        messages.success(request, 'compitition Deleted Successfully')
        return redirect('organization:view_compititions')
    messages.error(request, 'compitition Not Deleted')
    return redirect('organization:view_compititions')


def edit_workshop(request, workshop_id):
    workshop = Workshops.objects.get(id=workshop_id)
    if request.method == 'POST':
        workshop.name = request.POST.get('name')
        workshop.description = request.POST.get('description')
        workshop.date = request.POST.get('date')
        workshop.time = request.POST.get('time')
        workshop.location = request.POST.get('location')
        workshop.save()
        messages.success(request, 'workshop Updated Successfully')
        return redirect('organization:view_workshops')
    return render(request, 'organization/edit_workshop.html',{'workshop':workshop})

def delete_workshop(request, workshop_id):
    if Workshops.objects.get(id=workshop_id).delete():
        messages.success(request, 'workshop Deleted Successfully')
        return redirect('organization:view_workshops')
    messages.error(request, 'workshop Not Deleted')
    return redirect('organization:view_workshops')


def view_workshop_participants(request, workshop_id):
    if workshop_id:
        participants = Workshop_Participations.objects.filter(workshop=(Workshops.objects.get(id=workshop_id)))
        return render(request, 'organization/view_participants.html', {'participants':participants, 'event_mode':1})
    return render(request, 'organization/view_workshop_participants.html')


def view_event_participants(request, event_id):
    if request.method == 'GET':
        participants = Event_Participations.objects.filter(event=(Events.objects.get(id=event_id)))
        return render(request, 'organization/view_participants.html', {'participants':participants, 'event_mode':2})
    

def view_compitition_participants(request, compitition_id):
    if request.method == 'GET':
        participants = Compitition_Participations.objects.filter(compitition=(Compititions.objects.get(id=compitition_id)))
        return render(request, 'organization/view_participants.html', {'participants':participants, 'event_mode':3})
