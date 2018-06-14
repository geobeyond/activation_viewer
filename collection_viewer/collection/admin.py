from django.contrib import admin

from .models import DisasterType, Collection, MapSet, ExternalLayer, CollectionMaps, MapSetLayer


class CollectionInline(admin.TabularInline):
    model = MapSet
    filter_horizontal = ['layers']
    exclude = ['bbox_x0', 'bbox_x1', 'bbox_y1', 'bbox_y0']
    prepopulated_fields = {"slug": ("name",)}


class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionInline,]
    exclude = ['bbox_x0', 'bbox_x1', 'bbox_y1', 'bbox_y0']


class DisasterTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MapSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    exclude = ['bbox_x0', 'bbox_x1', 'bbox_y1', 'bbox_y0']
    filter_horizontal = ['layers']

admin.site.register(DisasterType, DisasterTypeAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(MapSet, MapSetAdmin)
admin.site.register(ExternalLayer)
admin.site.register(CollectionMaps)
admin.site.register(MapSetLayer)
