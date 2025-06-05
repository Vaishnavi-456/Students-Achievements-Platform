from django.db import models
from student.models import Student
# Create your models here.
class Organizations(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, primary_key=True)
    password = models.CharField(max_length=100, default='password')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    website = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Events(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TextField()
    location = models.TextField()
    certificate_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def registration_count(self):
        return Event_Participations.objects.filter(event=self).count()
    
class Workshops(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TextField()
    location = models.TextField()
    certificate_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def registration_count(self):
        return Workshop_Participations.objects.filter(workshop=self).count()
    
class Compititions(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TextField()
    location = models.TextField()
    certificate_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def registration_count(self):
        return Compitition_Participations.objects.filter(compitition=self).count()


class Event_Participations(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    participation_id = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.participation_id
    
class Workshop_Participations(models.Model):
    workshop = models.ForeignKey(Workshops, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    participation_id = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.participation_id

class Compitition_Participations(models.Model):
    compitition = models.ForeignKey(Compititions, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    participation_id = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.participation_id