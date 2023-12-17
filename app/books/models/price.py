from django.db import models

from utils.abstract import AbstractDateTimeModel, AbstractCreatedByModel
from utils.fields import PriceField

from .choices import BookPriceType


class BookPrice(AbstractCreatedByModel, AbstractDateTimeModel):
    type = models.CharField(
        max_length=14,
        choices=BookPriceType.choices
    )
    price = PriceField()
    book = models.ForeignKey(
        to="books.Book",
        related_name="prices",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Price for {self.book.title}"
