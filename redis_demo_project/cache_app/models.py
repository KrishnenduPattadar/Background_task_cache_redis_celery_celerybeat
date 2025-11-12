from django.db import models

ROLE_CHOICES = [
    ('EMPLOYEE','EMPLOYEE'),
    ('EXECUTIVE','EXECUTIVE'),
    ('MANAGER', 'MANAGER',)
]


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')


# --- ADD THIS LINE ---
    created_at = models.DateTimeField(auto_now_add=True) 
    # auto_now_add=True means Django will automatically set the
    # current time only when the employee is first created.
    def __str__(self):
        
        return f"{self.name} ({self.get_role_display()})"

    class Meta:
        ordering = ['name']