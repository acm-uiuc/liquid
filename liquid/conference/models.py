from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(User):
    company_name = models.CharField(max_length=70)
    invited = models.BooleanField(default=False)
    objects = UserManager()

@receiver(post_save, sender=Company)
def new_company(sender, **kwargs):
   company = kwargs['instance']
   if company.groups.filter(name='Company').count() == 0:
      group = DjangoGroup.objects.get(name="Company")
      company.groups.add(group)
      company.save()