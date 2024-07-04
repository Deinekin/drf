from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from materials.services import create_stripe_price, create_session_stripe
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class PaymentListAPIView(ListAPIView):
    """ Getting list of payments. """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "method_of_payment",
    )
    ordering_fields = ("date_of_payment",)


class PaymentCreateAPIView(CreateAPIView):
    """ Create payment. """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.sum)
        session_id, payment_link = create_session_stripe(price)
        payment.session_id = session_id
        payment.url = payment_link
        payment.save()


class UserCreateAPIView(CreateAPIView):
    """ Create user. """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """ Get list of users. """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailAPIView(RetrieveAPIView):
    """ Detail watch of user. """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """ Updating user. """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """ Delete user. """
    serializer_class = UserSerializer
