from email.policy import default
from django.db import models

class viewsofpages(models.Model):
    number_of_users_entered_to_homepage = models.IntegerField(default=0)
    number_of_users_entered_to_aboutus = models.IntegerField(default=0)
    number_of_users_entered_to_contactUs = models.IntegerField(default=0)
    number_of_users_entered_to_howitworks = models.IntegerField(default=0)




