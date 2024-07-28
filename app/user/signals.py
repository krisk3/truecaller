from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from true_number.models import Contact


@receiver(post_save, sender=User)
def create_user_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(
            user=instance, contact_name=instance.name, contact_phone=instance.phone
        )
