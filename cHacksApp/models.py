from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    email = models.EmailField()
    rank = models.IntegerField(null=True)




class Questions(models.Model):
    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    answer = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField()




class Mark(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked')
    answered = models.BooleanField(default=False)

@receiver (pre_save, sender=Mark)
def update_user_score(sender, instance, **kwargs):
    if instance.answered:
        instance.user.score += instance.question.weight
        instance.user.save()



