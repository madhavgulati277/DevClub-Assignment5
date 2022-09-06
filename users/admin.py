from django.contrib import admin
from .models import *
from grades.models import studentAdmin


admin.site.register(new_user )
admin.site.register(student , studentAdmin)
admin.site.register(instructor)




