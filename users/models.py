from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Город", help_text="Укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD = (
        ("cash", "Наличными"),
        ("card", "Картой"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
    )
    date_of_payment = models.DateField(auto_now_add=True, verbose_name="Дата платежа")
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
    )
    sum = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    method_of_payment = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD,
        default="card",
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(
        max_length=255, **NULLABLE, verbose_name="Номер сессии"
    )
    url = models.URLField(max_length=400, **NULLABLE, verbose_name="Ссылка на оплату")

    def __str__(self):
        return f"{self.user} {self.paid_course if self.paid_course else self.paid_lesson} {self.sum}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-date_of_payment",)
