from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=255, null=True)
    questions = models.ManyToManyField('Questions')
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)




class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        ordering = ["user_score__rank"]
    
    

class SchoolScore(models.Model):
    score = models.IntegerField(default=0)
    rank = models.IntegerField(null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_score')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_score')

    class Meta:
        unique_together = ('school', 'user',)


class Questions(models.Model):
    STATUS_CHOICES = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard')
    )

    QUESTION_TYPE = (
        ('Code', 'Code'),
        ('Downloadable', 'Downloadable'),
        ('InputFlag', 'InputFlag'),
        ('Select', 'Select'),

    )

    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    answer = models.CharField(max_length=255)
    description = models.TextField()
    question_type = models.CharField(
        max_length=13, choices=QUESTION_TYPE, default='InputFlag')
    category = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='E')
    file = models.FileField(blank=True)
    code = models.TextField(blank=True, null=True)




class Mark(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked')
    answered = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


@receiver (pre_save, sender=Mark)
def update_user_score(sender, instance, **kwargs):
    if instance.answered:
        instance.user.user_score.get(school=instance.school).score += instance.question.weight
        instance.user.save()

@receiver (pre_save, sender=Questions)
def update_answers(sender, instance, **kwargs):
    if instance.answer:
        instance.answer = instance.answer.lower().strip()
        
