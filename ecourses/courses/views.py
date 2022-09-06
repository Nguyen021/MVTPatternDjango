from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *


# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializers


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer

    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    # list(GET) -->xem ds khoa hoc
    # ...(POST) them khoa hoc
    # detail --. xem chi tiet khoa hoc
    # ...(PUT) --> cap nhap mot khoa hoc
    # ...(delete) --> xoa mot khoa hoc


def index(request):
    # return HttpResponse("Hello")
    return render(request, template_name='index.html', context={'name': 'Duong Trung Nguyen'})


def welcome(request, year):
    return HttpResponse("This is welcome page " + str(year))


def welcome2(request, year):
    return HttpResponse("WELCOME  " + str(year))


class ViewTest(View):
    def get(self, request):
        return HttpResponse("TEST GET")

    def post(self, request):
        pass
