from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

from mart.models import Categories, Tag, Materials, \
    Lengths, ColorsOption, SizesOption, Product, Reviews, Brands, Occasion, Images, Genre, Taga


class ImageAd(admin.TabularInline):
    model = Images


class ProductAdmins(admin.ModelAdmin):
    inlines = [ImageAd, ]


admin.site.register(Categories)
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

admin.site.register(Genre)
admin.site.register(Taga)
