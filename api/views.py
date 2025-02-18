from django.shortcuts import render,get_object_or_404
#from django.http import JsonResponse
from students.models import Students
from .serializers import StudentsSerializer,EmployeesSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from employees.models import Employees
from django.http import Http404
from rest_framework import mixins,generics,viewsets
from blogs.models import Blog,Comment
from blogs.serializers import BlogSerializer,CommentSerializer
from .paginations import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter,OrderingFilter

# Create your views here.
@api_view(['GET','POST'])
def studentsView(request):
    if request.method == 'GET':
        #get all students from the database
        students=Students.objects.all()
        serializer=StudentsSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer=StudentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#to get the data of single student using primary key
@api_view(['GET','PUT','DELETE'])    
def studentDetailView(request,pk):
    try:
        student=Students.objects.get(pk=pk)
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer=StudentsSerializer(student)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':# to update the data of a student
        serializer=StudentsSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':# to delete the data of a student
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#class based views
# class Employee(APIView):
#     def get(self,request):
#         employees=Employees.objects.all()
#         serializer=EmployeesSerializer(employees,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     # def post(self,request):
#     #     return Response(status=status.HTTP_201_CREATED)
#     def post(self,request):
#         serializer=EmployeesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class EmployeeDetail(APIView):#getting single employee data
#     def get_object(self,pk):
#         try:
#             return Employees.objects.get(pk=pk)
#         except Employees.DoesNotExist:
#             raise Http404
        
#     def get(self,request,pk):
#         employee=self.get_object(pk)
#         serializer=EmployeesSerializer(employee)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def put(self,request,pk):
#         employee=self.get_object(pk)
#         serializer=EmployeesSerializer(employee,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk):
#         employee=self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
#mixins
class Employee(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Employees.objects.all()
    serializer_class=EmployeesSerializer
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

#mixins    
class EmployeeDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):#retreving single employee data
    queryset=Employees.objects.all()
    serializer_class=EmployeesSerializer

    def get(self,request,pk):
        return self.retrieve(request,pk)
    
    def put(self,request,pk):
        return self.update(request,pk)
    
    def delete(self,request,pk):
        return self.destroy(request,pk)
"""

"""
#generics
class Employee(generics.ListAPIView,generics.CreateAPIView):#getting all employees data
    queryset=Employees.objects.all()
    serializer_class=EmployeesSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView ):#retreving single employee data
    queryset=Employees.objects.all()
    serializer_class=EmployeesSerializer
    lookup_field='pk'
"""

#viewsets
# class EmployeeViewSet(viewsets.ViewSet):
#     def list(self,request):
#         queryset=Employees.objects.all()
#         serializer=EmployeesSerializer(queryset,many=True)
#         return Response(serializer.data)

#     def create(self,request):
#         serializer=EmployeesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def retrieve(self,request,pk=None):
#         employee = get_object_or_404(Employees,pk=pk)
#         serializer=EmployeesSerializer(employee)
#         return Response(serializer.data,status=status.HTTP_200_OK)

#     def update(self,request,pk):
#         employee=get_object_or_404(Employees,pk=pk)
#         serializer=EmployeesSerializer(employee,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self,request,pk):
#         employee=get_object_or_404(Employees,pk=pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

#ModelViewSet
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employees.objects.all()
    serializer_class=EmployeesSerializer
    pagination_class=CustomPagination
    # filterset_fields=['designation']
    filterset_class=EmployeeFilter

class BlogsView(generics.ListCreateAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    filter_backends=[SearchFilter,  OrderingFilter]
    search_fields= ['blog_title','blog_body']#['^blog_title']
    ordering_fields=['id','blog_title']

class CommentsView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='pk'

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    lookup_field='pk'
    