from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=255, null=True)
    questions = models.ManyToManyField('Questions')
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def ___str__(self):
        return self.name


class CustomUserManager(BaseUserManager): # 1.

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

        # user.set_password(password)
        # user.save(using=self._db)
        # return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    
    changed_password = models.BooleanField(default=False)

    email = models.EmailField(unique=True) # 3.

    # username = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    # REQUIRED_FIELDS = [] # 6.

    class Meta:
        ordering = ["-user_score__score"]


    def __str__(self):
        return self.email
    
    

class SchoolScore(models.Model):
    score = models.IntegerField(default=0)
    # rank = models.IntegerField(null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_score')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_score')

    class Meta:
        unique_together = ('school', 'user',)

    def __str__(self):
        return f"{self.score} for {self.school}"


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


class Notification(models.Model):
   # title = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Mark(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked')
    answered = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


@receiver (pre_save, sender=Mark)
def update_user_score(sender, instance, **kwargs):
    if instance.answered:
        obj, _ = instance.user.user_score.get_or_create(school=instance.school)
        obj.score += instance.question.weight
        obj.save()
        

@receiver (pre_save, sender=Questions)
def update_answers(sender, instance, **kwargs):
    if instance.answer:
        instance.answer = instance.answer.lower().strip()
        instance.encoded = "".join(["*" if c not in [" ", '.'] else c for c in instance.answer])

        