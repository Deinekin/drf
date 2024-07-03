from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(link='video_link')]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    quantity_of_lessons = SerializerMethodField()
    is_subscribe = SerializerMethodField()

    @staticmethod
    def get_quantity_of_lessons(obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribe(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = ("name", "description", "quantity_of_lessons", "lessons", "is_subscribe")


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(source="lesson_set", many=True)

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
