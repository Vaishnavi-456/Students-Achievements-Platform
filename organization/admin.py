from django.contrib import admin
from .models import Organizations, Events, Workshops, Compititions, Event_Participations, Workshop_Participations, Compitition_Participations
# Register your models here.

admin.site.register(Organizations)
admin.site.register(Events)
admin.site.register(Workshops)
admin.site.register(Compititions)
admin.site.register(Event_Participations)
admin.site.register(Workshop_Participations)
admin.site.register(Compitition_Participations)