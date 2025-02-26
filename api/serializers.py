from rest_framework import serializers
from students.models import Students
from employees.models import Employees
import re

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Students
        fields='__all__'

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employees
        fields='__all__'

    def validate_emp_name(self, value):
        if 'admin' in value.lower():
            raise serializers.ValidationError("Name cannot contain 'admin'")
        return value
    
    def validate_emp_id(self, value):
        if not re.match(r'^EMP\d+$', value):
            raise serializers.ValidationError("Employee ID must start with 'EMP' followed by digits.")
        return value
    
    