from django.contrib import admin
from django import forms
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from tinymce.widgets import TinyMCE

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


class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        widgets = {
            'description_long': TinyMCE(),
        }


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    form = PlaceAdminForm
    inlines = [PlaceImageInline]
    list_display = ['title']


@admin.register(PlaceImage)
class PlaceImageAdmin(PlaceImagePreviewMixin, admin.ModelAdmin):
    list_display = ['__str__', 'get_preview']
    fields = ['place', 'image', 'get_preview']
    readonly_fields = ['get_preview']
