from django.db import models
from django.utils import timezone

from datetime import timedelta

import binascii
from os import urandom as generate_bytes

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

# Create your models here.

class Token(models.Model):
    def random_string():
        return str(binascii.hexlify(generate_bytes(6)).decode())
    created = models.DateTimeField(auto_now_add=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True, default=timezone.now()+timedelta(hours=10))
    key = models.CharField(primary_key=True, default=random_string)
    user = models.ForeignKey('auth.User', related_name='verificationtokens', on_delete = models.CASCADE)

    class Meta:
        abstract = True

class VerificationToken(Token):
    pass
