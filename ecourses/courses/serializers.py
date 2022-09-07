from rest_framework.decorators import action
from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'avatar', 'email']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CourseSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'updated_date', 'category']


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializers(ModelSerializer):
    """
      A viewset for viewing and editing user instances.
    """
    tags = TagSerializers(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'content', 'created_date', 'course', 'tags']
