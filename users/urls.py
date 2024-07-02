from django.urls import path
from rest_framework.routers import SimpleRouter


from users.views import (PaymentListAPIView, PaymentCreateAPIView)
from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
]

urlpatterns += router.urls
