from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from .views import *
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('Course', views.CourseViewSet)

router.register('Lesson', views.LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.index, name="index"),
    path('welcome/<int:year>/', views.welcome, name="welcome"),
    path('admin/', admin.site.urls),
    # path('admin/', admin_site.urls),

    path('test/', views.ViewTest.as_view()),
    re_path(r'^welcome2/(?P<year>[0-9]{4})/$', views.welcome2, name='welcome2')
]
