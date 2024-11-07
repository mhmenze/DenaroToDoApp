from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    due_time = models.TimeField()
    completed = models.BooleanField(default=False)
    assigned_email = models.EmailField(max_length=254, blank=True, null=True, help_text="Email of the assignee")


class User(models.Model):
    username = models.CharField(max_length=35)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.title}'
