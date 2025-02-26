from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Employees
from datetime import datetime

class EmployeeAPITestCase(APITestCase):
    
    def setUp(self):
        # Create an employee instance that will be used for the PUT and DELETE tests
        self.employee_data = {
            'emp_id': 'EMP001',
            'emp_name': 'John Doe',
            'designation': 'Manager',
            'hire_date': '2025-02-11'
        }
        self.employee = Employees.objects.create(**self.employee_data)
        self.list_url = reverse('employee-list')
        self.detail_urls = reverse('employee-detail', kwargs={'pk': self.employee.pk})

    def test_get_employees(self):
        # Test the GET method to retrieve all employees
        response = self.client.get(self.list_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       
    def test_post_employee(self):
        # Test the POST method to create a new employee
        new_employee_data = {
            'emp_id': 'EMP002',
            'emp_name': 'Jane Smith',
            'designation': 'Engineer',
            'hire_date': '2025-02-15',
        }
        response = self.client.post(self.list_url, new_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_employee(self):
        # Test the PUT method to update an existing employee
        updated_data = {
            'emp_id': 'EMP001',
            'emp_name': 'Johnathan Doe',  # Updating name
            'designation': 'Senior Manager',
            'hire_date': '2025-02-10',  # Updating hire date
        }
        response = self.client.put(self.detail_urls, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee(self):
        response = self.client.get(self.detail_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure employee exists
        response = self.client.delete(self.detail_urls)#delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.list_url)#checking if employee is deleted
        print(response.data)  # Debugging

    #extra testing
    def test_post_employee_missing_name(self):
    # Missing 'emp_name'
        new_employee_data = {
            'emp_id': 'EMP003',
            'designation': 'Engineer',
            'hire_date': '2025-02-20',
        }
        response = self.client.post(self.list_url, new_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emp_name', response.data)  # Check if error on 'emp_name'

    def test_post_employee_duplicate_emp_id(self):
        self.client.post(self.list_url, self.employee_data, format='json')

        new_employee_data = {
            'emp_id': 'EMP001',  # Duplicate emp_id
            'emp_name': 'Duplicate John',
            'designation': 'Manager',
            'hire_date': '2025-02-20',
        }
        response = self.client.post(self.list_url, new_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emp_id', response.data)  # Error related to duplicate emp_id

    


    