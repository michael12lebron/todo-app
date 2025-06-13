from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(null=True, blank=True)
    due_date=models.DateField(null=True, blank=True)
    priority = models.CharField(                                 # 🆕 Low/Med/High
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    is_completed = models.BooleanField(default=False)
    notes=models.TextField(blank=True)

    def __str__(self):
        return self.title



