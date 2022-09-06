from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from grades.models import course
from quiz.models import mcq_question, question_bank , subjective_question

@receiver(post_save ,sender = course)
def create_qb(sender , instance , created , **kwargs):
    if created:
        qb = question_bank(course = instance)
        qb.save()

@receiver(post_save ,sender = mcq_question)
def create_qb(sender , instance , created , **kwargs):
    if created:
        instance.mcq_flag = True
        instance.save()

@receiver(post_save ,sender = subjective_question)
def create_qb(sender , instance , created , **kwargs):
    if created:
        instance.mcq_flag = False
        instance.save()



