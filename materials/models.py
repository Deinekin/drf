from django.db import models

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    preview_image = models.ImageField(
        upload_to="course_images", verbose_name="Фото", **NULLABLE
    )

    def __str__(self):
        return f"{self.name} {self.description[:100]}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    preview_image = models.ImageField(
        upload_to="course_images", verbose_name="Фото", **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", **NULLABLE
    )
    video_link = models.URLField(verbose_name="Ссылка на видеоурок", **NULLABLE)

    def __str__(self):
        return f"{self.name} {self.description[:100]}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
