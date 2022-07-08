from django.contrib import admin
from eventhandler.models import CustomUser, EventTracker


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(EventTracker)
