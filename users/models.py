from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .managers import UserManager


def avatar_path(instance, filename):
    return f"avatars/user_{instance.pk or 'new'}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    name = models.CharField("имя", max_length=124)
    surname = models.CharField("фамилия", max_length=124)
    avatar = models.ImageField("аватар", upload_to=avatar_path, blank=True)
    phone = models.CharField("телефон", max_length=12, unique=True, blank=True, null=True)
    github_url = models.URLField("GitHub", blank=True)
    about = models.TextField("о себе", max_length=256, blank=True)
    favorites = models.ManyToManyField(
        "projects.Project",
        blank=True,
        related_name="interested_users",
        verbose_name="избранные проекты",
    )
    is_active = models.BooleanField("активен", default=True)
    is_staff = models.BooleanField("администратор", default=False)
    date_joined = models.DateTimeField("дата регистрации", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ["id"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.name} {self.surname} <{self.email}>"

    def save(self, *args, **kwargs):
        create_avatar = not self.avatar or not self.avatar.storage.exists(self.avatar.name)
        super().save(*args, **kwargs)

        if create_avatar:
            self.avatar.save(
                f"avatar_{self.pk}.png",
                self._build_avatar_file(),
                save=False,
            )
            super().save(update_fields=["avatar"])

    def _build_avatar_file(self):
        palette = ["#8FAADC", "#93C47D", "#F6B26B", "#C9A0DC", "#76A5AF"]
        color = palette[self.pk % len(palette)]
        letter = (self.name[:1] or self.email[:1] or "?").upper()

        image = Image.new("RGB", (256, 256), color)
        drawer = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 132)
        except OSError:
            font = ImageFont.load_default()

        box = drawer.textbbox((0, 0), letter, font=font)
        x = (256 - (box[2] - box[0])) / 2
        y = (256 - (box[3] - box[1])) / 2 - 8
        drawer.text((x, y), letter, fill="#FFFFFF", font=font)

        output = BytesIO()
        image.save(output, format="PNG")
        return ContentFile(output.getvalue())

