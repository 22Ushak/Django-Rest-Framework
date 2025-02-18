from rest_framework import serializers
from students.models import Students
from employees.models import Employees

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Students
        fields='__all__'

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employees
        fields='__all__'