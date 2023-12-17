from django.db import models

from utils.abstract import AbstractDateTimeModel, AbstractCreatedByModel


class Author(AbstractDateTimeModel, AbstractCreatedByModel):
    first_name = models.CharField(
        max_length=255,
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
