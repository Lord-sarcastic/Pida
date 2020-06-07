from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Key(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digit = models.CharField(max_length=1024, blank=True)
    start = models.IntegerField()
    end = models.IntegerField()

    def __str__(self):
        return f'{self.username}'

    def clean(self, *args, **kwargs):
        if self.end <= self.start:
            raise ValidationError(_("Start value should be less than end value"))
        return super().clean(*args, **kwargs)