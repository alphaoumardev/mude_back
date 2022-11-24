from django.contrib import admin
from mart.models import Categories, Tag, Materials, \
    Lengths, ColorsOption, SizesOption, Product, Reviews, Brands, Occasion, Images

admin.site.register(Categories)
admin.site.register(Tag)
admin.site.register(Materials)
admin.site.register(Lengths)
admin.site.register(ColorsOption)
admin.site.register(SizesOption)
admin.site.register(Brands)
admin.site.register(Occasion)
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Reviews)

