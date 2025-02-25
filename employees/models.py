from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.
class Employees(models.Model):
    emp_id=models.CharField(max_length=10,blank=False, null=False)
    emp_name=models.CharField(max_length=50,blank=False, null=False)
    designation=models.CharField(max_length=50,blank=False, null=False)

    hire_date=models.DateField(default=datetime.now)

    def clean(self):
        # Custom validation to ensure emp_id is not longer than 10 characters
        if len(self.emp_id) > 10:
            raise ValidationError("Employee ID cannot exceed 10 characters.")

    
    
    def __str__(self):
        return self.emp_name