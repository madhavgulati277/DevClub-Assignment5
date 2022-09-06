from django.contrib import admin
from .models import courseAdmin, grades,course

admin.site.register(grades)
admin.site.register(course,courseAdmin)

