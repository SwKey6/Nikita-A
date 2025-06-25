from django.contrib import admin
from .models import Employee, Service, Appointment, Review

admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Review)