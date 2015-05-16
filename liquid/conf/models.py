from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(User):
    STARTUP = "S"
    JOBFAIR = "J"
    TYPE_CHOICES = ((STARTUP, "Startup Company"), (JOBFAIR, "Job Fair Company"))

    company_name = models.CharField(max_length=70)
    type = models.CharField(choices=TYPE_CHOICES, default=JOBFAIR, max_length=1)
    invited = models.BooleanField(default=False)
    invited_on = models.DateField(blank=True, null=True)
    invited_by = models.ForeignKey(User, blank=True, null=True, related_name="jobfair_invite")
    objects = UserManager()

@receiver(post_save, sender=Company)
def new_company(sender, **kwargs):
   company = kwargs['instance']
   if company.groups.filter(name='Company').count() == 0:
      group = DjangoGroup.objects.get(name="Company")
      company.groups.add(group)
      company.save()