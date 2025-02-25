from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router=DefaultRouter()
router.register('employees',views.EmployeeViewSet,basename='employee')

urlpatterns = [
    path('students/', views.studentsView),
    path('students/<int:pk>/', views.studentDetailView),

    #class based views
    # path('employees/', views.Employee.as_view()),
    # path('employees/<int:pk>/',views.EmployeeDetail.as_view()),

    path('',include(router.urls)),

    path('blogs/',views.BlogsView.as_view()),
    path('comments/',views.CommentsView.as_view()),

    path('blogs/<int:pk>/',views.BlogDetailView.as_view()),
    path('comments/<int:pk>/',views.CommentDetailView.as_view()),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # generates the OpenAPI schema
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),  # Redoc UI

]


