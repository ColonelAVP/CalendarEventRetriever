from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import (
    Model,
    TextField,
    BooleanField,
    EmailField,
    CharField,
    JSONField,
    ForeignKey,
)

from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user Model --> stores user information in respective fields
    """

    email = EmailField(_("email address"), unique=True)
    first_name = CharField(max_length=100, null=True, blank=True)
    middle_name = CharField(max_length=100, null=True, blank=True)
    last_name = CharField(max_length=100, null=True, blank=True)
    google_token = JSONField(blank=True, null=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)
    remark = TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)


class EventTracker(Model):
    """
    Event Tracker Model --> stores calendar events of the user
    """

    user = ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_events")
    events = JSONField(default=dict)
    remark = TextField(blank=True, null=True)
    created_date = CreationDateTimeField(null=True)
    updated_date = ModificationDateTimeField(null=True)

    def __str__(self) -> str:
        # pylint: disable=E1101
        return f"{self.user.email}"
