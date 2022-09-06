from rest_framework.decorators import action
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.response import Response
from rest_framework import status


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'updated_date', 'category']


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializers(ModelSerializer):
    tags = TagSerializers(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'content', 'created_date', 'course', 'tags']

    @action(methods=['post'], detail=True, url_path="hide-lesson", url_name="hide-lesson")
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=LessonSerializers(l).data, status=status.HTTP_200_OK)
