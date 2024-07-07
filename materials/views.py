from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from materials.tasks import send_course_change
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """ViewSet of Course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()
        send_course_change.delay(course.pk)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModerator,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Class creating."""

    serializer_class = LessonSerializer

    permission_classes = (
        ~IsModerator,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Getting list of lessons"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonUpdateAPIView(UpdateAPIView):
    """Update lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsModerator | IsOwner,
        IsAuthenticated,
    )


class LessonRetrieveAPIView(RetrieveAPIView):
    """Detail watch lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsModerator | IsOwner,
        IsAuthenticated,
    )


class LessonDestroyAPIView(DestroyAPIView):
    """Delete lesson."""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)
    queryset = Lesson.objects.all()


class SubscriptionCreateAPIView(APIView):
    """Create/Delete subscription."""

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
