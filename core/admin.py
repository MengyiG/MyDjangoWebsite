from django.contrib import admin

# Register your models here.
from .models import Channel, Topic, Message

admin.site.register(Channel)
admin.site.register(Topic)
admin.site.register(Message)
