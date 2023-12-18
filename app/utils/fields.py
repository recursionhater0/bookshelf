from django.db import models


class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 10
        kwargs["decimal_places"] = 2
        super().__init__(*args, **kwargs)
