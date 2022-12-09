from django.contrib.admin import register, ModelAdmin

from corn.models import Corn


@register(Corn)
class CornAdmin(ModelAdmin):
    list_display = ["year", "corn_yield"]
    list_filter = [
        "year",
    ]
    ordering = [
        "year",
    ]
