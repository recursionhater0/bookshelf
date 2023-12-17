from django.db import models


class BookPriceType(models.TextChoices):
    PRODUCER_PRICE = "PRODUCER_PRICE"
    RETAIL_PRICE = "RETAIL_PRICE"
