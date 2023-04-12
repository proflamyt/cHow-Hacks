from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.dispatch import Signal

notification_created = Signal()

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=255, null=True)
    questions = models.ManyToManyField('Questions')
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name




class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    
    changed_password = models.BooleanField(default=False)

    email = models.EmailField(unique=True) 

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    

    class Meta:
        ordering = ["-user_score__score"]


    def __str__(self):
        return self.email
    
    

class SchoolScore(models.Model):
    score = models.IntegerField(default=0)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_score')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_score')

    class Meta:
        unique_together = ('school', 'user',)

    def __str__(self):
        return f"{self.score}pts for {self.user.username}"


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
    weight = models.IntegerField(default=1)
    answer = models.CharField(max_length=255)
    description = models.TextField()
    question_type = models.CharField(
        max_length=13, choices=QUESTION_TYPE, default='InputFlag')
    encoded = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='E')
    file = models.FileField(blank=True)
    code = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} : {self.description[:10]}..."


class Notification(models.Model):
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Send the notification_created signal when a new notification is saved
        notification_created.send(sender=self.__class__, notification=self)


class Mark(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked')
    answered = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} for {self.question.name}"


  