from rest_framework.generics import (CreateAPIView, ListAPIView)
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from users.serializers import PaymentSerializer
from users.models import Payment


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('paid_course', 'paid_lesson', 'method_of_payment',)
    ordering_fields = ('date_of_payment',)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
