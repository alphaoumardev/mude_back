from django.contrib.auth.models import User, AbstractUser
from django.utils.safestring import mark_safe

from customers.models import CustomerProfile

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# class Categories(models.Model):
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcates", )
#     name = models.CharField(max_length=30, null=True, blank=True, )
#
#     def __str__(self):
#         cate = [self.name]
#         root = self.parent
#         while root is not None:
#             cate.append(root.name)
#             root = root.parent
#         return " -> ".join(cate[::-1])
#
#     class Meta:
#         verbose_name_plural = 'Categories'
#
#     @property
#     def child_article(self):
#         return self.article.filter(category=self).order_by('category_id').reverse()
#
#     def children(self):  # subcategories
#         return Categories.objects.filter(parent=self)
#
#     @property
#     def is_parent(self):
#         if self.parent is not None:
#             return False
#         return True


class Category(MPTTModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcates')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    def __str__(self):
        return self.tag_name


class Materials(models.Model):
    material_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    def __str__(self):
        return self.material_name

    class Meta:
        verbose_name_plural = "Matrials"


class Lengths(models.Model):
    length_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    def __str__(self):
        return self.length_name

    class Meta:
        verbose_name_plural = "Lengths"


class ColorsOption(models.Model):
    color_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    def __str__(self):
        return self.color_name


class SizesOption(models.Model):
    size_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    def __str__(self):
        return self.size_name


class Brands(models.Model):
    brand_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    class Meta:
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.brand_name


class Occasion(models.Model):
    occasion_name = models.CharField(blank=True, null=True, max_length=15, unique=True)

    def __str__(self):
        return self.occasion_name

    class Meta:
        verbose_name_plural = "Occasions"


class Product(models.Model):
    SALES = (("Sale", "Sale"), ("New", "New"), ("Regular", "Regular"))
    category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name="articles", null=True, blank=True)

    # category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="article")
    name = models.CharField(max_length=50, null=False)
    sku = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=False)
    price = models.DecimalField(default=20, decimal_places=2, max_digits=6)

    status = models.BooleanField(default=True, null=True, )
    stock = models.IntegerField(default=50)
    onsale = models.CharField(null=True, blank=True, choices=SALES, max_length=10)
    discount = models.DecimalField(decimal_places=2, max_digits=3, default=1, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ManyToManyField(ColorsOption, related_name="colored", blank=True)
    size = models.ManyToManyField(SizesOption, related_name="sized", blank=True)
    slide = models.ManyToManyField("self", related_name="slided", symmetrical=False, blank=True)
    tag = models.ManyToManyField(Tag, related_name="tagged", blank=True)
    lengths = models.ManyToManyField(Lengths, related_name="lened", blank=True)
    materials = models.ManyToManyField(Materials, related_name="materialized", blank=True)
    occasion = models.ManyToManyField(Occasion, related_name="occusioned", blank=True)

    def __str__(self):
        return self.name

    @property
    def images(self):
        return self.images_set.all()

    @property
    def review(self):
        return self.reviews_set.all()


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to="assets/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.product.name

    def image_preview(self):
        if self.image:
            return mark_safe(
                '<img src="{}" style="width: 50px; height:50px; object-fit:contain;" />'.format(self.image.url))
        else:
            return 'No image found'

    image_preview.short_description = "Image"


class Reviews(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=400, blank=True, null=True)
    rate = models.IntegerField(default=1)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class FuturedImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image_url = models.ImageField(upload_to="mudi", blank=True, null=True)
    color_name = models.ForeignKey("ColorsOption", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.image_url.url

    class Meta:
        verbose_name_plural = 'Detail Images'
