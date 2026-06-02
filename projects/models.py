from django.conf import settings
from django.db import models


class Project(models.Model):
    OPEN = "open"
    CLOSED = "closed"
    STATUS_CHOICES = (
        (OPEN, "Open"),
        (CLOSED, "Closed"),
    )

    name = models.CharField("название", max_length=200)
    description = models.TextField("описание", blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="автор",
    )
    created_at = models.DateTimeField("дата создания", auto_now_add=True, db_index=True)
    github_url = models.URLField("GitHub", blank=True)
    status = models.CharField(
        "статус",
        max_length=6,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="participated_projects",
        verbose_name="участники",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.name

    @property
    def is_open(self):
        return self.status == self.OPEN

