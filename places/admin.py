from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from .models import Place, PlaceImage


class PlaceImagePreviewMixin:
    @staticmethod
    def get_preview(obj):
        if not obj or not obj.image:
            return '-'

        return format_html(
            '<img src="{}" style="max-height: 200px; width: auto;" />',
            obj.image.url,
        )

    get_preview.short_description = 'Get preview'


class PlaceImageInline(SortableInlineAdminMixin, PlaceImagePreviewMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ['image', 'get_preview']
    readonly_fields = ['get_preview']
    sortable_field_name = 'position'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInline]
    list_display = ['title']


@admin.register(PlaceImage)
class PlaceImageAdmin(PlaceImagePreviewMixin, admin.ModelAdmin):
    list_display = ['__str__', 'get_preview']
    fields = ['place', 'image', 'get_preview']
    readonly_fields = ['get_preview']
