from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from common.models import BaseModel


class Corn(BaseModel):
    """
    Corn model is used to store US corn yield data
    """

    year = models.PositiveSmallIntegerField(
        unique=True, help_text="Year of the harvest"
    )
    corn_yield = models.IntegerField(
        help_text="Corn grain yield in the United States (measured in 1000s of megatons)"
    )

    objects = BulkUpdateOrCreateQuerySet.as_manager()
