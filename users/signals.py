from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import student,instructor,new_user

# @receiver(post_save , sender = User)
# def create_new_user(sender , instance , created , **kwargs):
#     if created:
#         new_user.objects.create(user = instance)

# @receiver(post_save , sender = User)
# def save_new_user(sender , instance , **kwargs):
#     instance.new_user.save()






@receiver(post_save ,sender = new_user)
def create_profile(sender , instance , created , **kwargs):
    if created:
        if instance.is_student:
            student.objects.create(user = instance)
        if instance.is_instructor:
            instructor.objects.create(user = instance)


@receiver(post_save ,sender = new_user )
def save_profile(sender , instance , **kwargs):
    if (instance.is_student):
        instance.student.save()
    if (instance.is_instructor):
        instance.instructor.save()




    