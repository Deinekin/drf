from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(source="lesson_set", many=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    quantity_of_lessons = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True)

    @staticmethod
    def get_quantity_of_lessons(obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ("name", "description", "quantity_of_lessons", "lessons")
