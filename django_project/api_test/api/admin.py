from django.contrib import admin

from .models import Users, Question

admin.site.register(Users)
admin.site.register(Question)