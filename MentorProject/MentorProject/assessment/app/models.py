from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Mentor(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=68)
    registration_date = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', 'role']
    available_permissions = {
        'reply_question': True,
        'post_question': True,
    }

    def __str__(self):
        return self.email


class NewUser(AbstractBaseUser):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, db_column="mentor")
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=68)
    registration_date = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', 'role']
    available_permissions = {
        'reply_question': False,
        'post_question': True,
    }

    def __str__(self):
        return self.email


class Questions(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, db_column='user')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, db_column='mentor')
    question = models.CharField(null=False, blank=False, max_length=1000)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    message = models.CharField(null=True, blank=True, max_length=1000)
    file_name = models.CharField(null=True, blank=True, max_length=100)
    file = models.FileField(upload_to='', null=True, blank=True)
    post_time = models.DateTimeField(null=True, blank=True)
    replied_time = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ['question']
    verbose = "Questions"
    verbose_name = 'Question',

    class Meta:
        unique_together = ('user', 'mentor', 'question')


