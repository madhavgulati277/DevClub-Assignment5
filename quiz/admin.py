from django.contrib import admin
from .models import *

admin.site.register(question)
admin.site.register(subjective_question)
admin.site.register(mcq_question)
admin.site.register(question_bank)
admin.site.register(quiz)
admin.site.register(quiz_grade)



