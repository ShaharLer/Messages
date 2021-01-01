from django.db import models
from datetime import date


class SystemUser(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(SystemUser, related_name='sender', blank=False, on_delete=models.CASCADE)
    receiver = models.ForeignKey(SystemUser, related_name='receiver', blank=False, on_delete=models.CASCADE)
    subject = models.CharField(max_length=32, blank=False)
    message = models.TextField(max_length=256, blank=False)
    created = models.DateField('Date created', default=date.today())
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject}'
