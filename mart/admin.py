from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from mart.models import *


class ImageAd(admin.TabularInline):
    model = Images


class ProductAdmins(admin.ModelAdmin):
    inlines = [ImageAd, ]


admin.site.register(Tag)
admin.site.register(Materials)
admin.site.register(Lengths)
admin.site.register(ColorsOption)
admin.site.register(SizesOption)
admin.site.register(Brands)
admin.site.register(Occasion)
admin.site.register(Product, ProductAdmins)
admin.site.register(Images)
admin.site.register(Reviews)

admin.site.register(Category, DraggableMPTTAdmin)
