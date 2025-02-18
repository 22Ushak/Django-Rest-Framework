from django.shortcuts import render,HttpResponse

# Create your views here.
def students(request):
    students=[
        {'id':1,'name':'John','age':23},
        {'id':2,'name':'Doe','age':24},
        {'id':3,'name':'Smith','age':25}
    ]
    return HttpResponse(students)