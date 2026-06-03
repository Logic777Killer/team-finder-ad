from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from common.constants import (
    AVATAR_COLORS,
    AVATAR_FONT_NAME,
    AVATAR_FONT_SIZE_RATIO,
    AVATAR_FORMAT,
    AVATAR_MODE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)

from .managers import UserManager


def avatar_path(instance, filename):
    return f"avatars/user_{instance.pk or 'new'}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    name = models.CharField("имя", max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField("фамилия", max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField("аватар", upload_to=avatar_path, blank=True)
    phone = models.CharField(
        "телефон",
        max_length=USER_PHONE_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
    )
    github_url = models.URLField("GitHub", blank=True)
    about = models.TextField("о себе", max_length=USER_ABOUT_MAX_LENGTH, blank=True)
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
        ordering = ["-date_joined"]
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
        color = AVATAR_COLORS[self.pk % len(AVATAR_COLORS)]
        letter = (self.name[:1] or self.email[:1] or "?").upper()

        image = Image.new(AVATAR_MODE, (AVATAR_SIZE, AVATAR_SIZE), color)
        drawer = ImageDraw.Draw(image)
        font_size = int(AVATAR_SIZE * AVATAR_FONT_SIZE_RATIO)

        try:
            font = ImageFont.truetype(AVATAR_FONT_NAME, font_size)
        except OSError:
            font = ImageFont.load_default(size=font_size)

        box = drawer.textbbox((0, 0), letter, font=font)
        text_width = box[2] - box[0]
        text_height = box[3] - box[1]
        x = (AVATAR_SIZE - text_width) / 2 - box[0]
        y = (AVATAR_SIZE - text_height) / 2 - box[1]
        drawer.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)

        output = BytesIO()
        image.save(output, format=AVATAR_FORMAT)
        return ContentFile(output.getvalue())

