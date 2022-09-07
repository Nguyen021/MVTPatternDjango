from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions, generics, status
from .models import *
from .serializers import UserSerializer, LessonSerializers, CourseSerializer

from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action


class UserViewSet(viewsets.ViewSet,

                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializers

    @action(detail=True, methods=['post'], url_path='hide-lesson', url_name='hide-lesson', )
    # default lesson/pk/ hide_lesson
    def hide_lesson(self, request, pk=None):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=LessonSerializers(l, context={'request': request}).data, status=status.HTTP_200_OK)


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
