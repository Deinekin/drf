from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, link):
        self.link = link

    def __call__(self, value):
        video_link = dict(value).get(self.link)
        if video_link:
            if "youtube.com" not in video_link:
                raise ValidationError("Можно размещать ссылки только на youtube")
