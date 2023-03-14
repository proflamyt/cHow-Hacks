from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Mark, Questions

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
        instance.encoded = "".join(["*" if c not in [" ", '.', '/', ':'] else c for c in instance.answer])

      