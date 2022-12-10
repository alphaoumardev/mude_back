from rest_framework import serializers

from mart.models import Categories, Tag, Materials, Product, ColorsOption, Lengths, SizesOption, Reviews, Images, \
    Brands, Occasion


class ArticleSerializer(serializers.ModelSerializer):
    model = Product
    fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    subcates_count = serializers.SerializerMethodField()
    # articles = ArticleSerializer(many=True,read_only=True, source="Product_set")

    class Meta:
        model = Categories
        fields = '__all__'
        depth = 1

    # @staticmethod
    # def get_articles(obj):
    #     pro = Product.objects.select_related("category")
    #     return ProductSerializer(pro, many=True).data

    def get_fields(self):
        fields = super(CategoriesSerializer, self).get_fields()
        fields['subcates'] = CategoriesSerializer(many=True)
        return fields

    @staticmethod
    def get_subcates_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return obj.subcates.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ["brand_name"]


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ["material_name"]


class ColorsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorsOption
        fields = ["color_name"]


class LengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lengths
        fields = ["length_name"]


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ["occasion_name"]


class SizeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SizesOption
        fields = ["size_name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["image"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1
    """Remember when the model does not have the field to add it here"""
    images = ImageSerializer(read_only=True, many=True)

    # category = CategoriesSerializer(many=False, read_only=True,)# source='category_set'
    # tag = TagSerializer(read_only=True, many=True, required=False)
    # brand = BrandSerializer(read_only=True, required=False, many=False)
    # color = ColorsOptionSerializer(read_only=True, required=False, many=True)
    # size = SizeSerialiser(read_only=True, required=False, many=True)
    # lengths = LengthSerializer(read_only=True, required=False, many=True)
    # materials = MaterialSerializer(read_only=True, required=False, many=True)
    # occasion = OccasionSerializer(read_only=True, required=False, many=True)

    # @staticmethod
    # def get_images(obj):
    #     return


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
