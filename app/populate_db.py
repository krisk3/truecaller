import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()

import random
from user.models import User
from true_number.models import Contact, SpamContact
from faker import Faker

fakegen = Faker()


def populate(N=5):
    for entry in range(N):
        fake_name = fakegen.name()
        fake_phone = fakegen.msisdn()
        password = "Password@123"

        user = User.objects.create_user(
            name=fake_name, phone=fake_phone, password=password
        )
        for i in range(random.randint(0, 10)):
            fake_con_name = fakegen.name()
            fake_con_phone = fakegen.msisdn()
            Contact.objects.create(
                user=user, contact_name=fake_con_name, contact_phone=fake_con_phone
            )

        for i in range(random.randint(0, 5)):
            fake_spam_phone = fakegen.msisdn()
            spam_contact = SpamContact.objects.create(spam_phone=fake_spam_phone)
            spam_contact.spammed_by_users.add(user)


if __name__ == "__main__":
    print("Populating the database.\nPlease wait...")
    populate(50)
    print("Populating successful!")
