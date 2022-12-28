from rest_framework import serializers
from customers.serializers import CustomerProfileSerializer
from mart.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'name', 'parent', 'subcates']
        depth = 4

    def get_fields(self):
        """
        :return:
        """
        fields = super(CategorySerializer, self).get_fields()
        fields['subcates'] = CategorySerializer(many=True)
        return fields

    """# @staticmethod
    # def get_parent(obj):
    #     if obj.parent is not None:
    #         return CategorySerializer(obj.parent).data
    #     else:
    #         return None
    """


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "tag_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ["id", "brand_name"]


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ["id", "material_name"]


class ColorsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorsOption
        fields = ["id", "color_name"]


class LengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lengths
        fields = ["id", "length_name"]


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ["id", "occasion_name"]


class SizeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SizesOption
        fields = ["id", "size_name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 4

    """Remember when the model does not have the field to add it here"""

    images = ImageSerializer(read_only=True, many=True)
    reviews = serializers.SerializerMethodField()

    @staticmethod
    def get_reviews(obj):
        return ReviewReadSerializer(obj.review, many=True).data
    """
    # images = serializers.SerializerMethodField()
    #
    # @staticmethod
    # def get_images(obj):
    #     return ImageSerializer(obj.image, many=True).data
    """
    # category = CategorySerializer(many=False, read_only=True,) # source='category_set'
    # tag = TagSerializer(read_only=True, many=True, required=False)
    # brand = BrandSerializer(read_only=True, required=False, many=False)
    # color = ColorsOptionSerializer(read_only=True, required=False, many=True)
    # size = SizeSerialiser(read_only=True, required=False, many=True)
    # lengths = LengthSerializer(read_only=True, required=False, many=True)
    # materials = MaterialSerializer(read_only=True, required=False, many=True)
    # occasion = OccasionSerializer(read_only=True, required=False, many=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"


class ReviewReadSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(required=False, read_only=True)

    class Meta:
        model = Reviews
        fields = "__all__"
        # depth = 2
