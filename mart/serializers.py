from rest_framework import serializers

from customers.serializers import CustomerProfileSerializer
from mart.models import Categories, Tag, Materials, Product, ColorsOption, Lengths, SizesOption, Reviews, Images, \
    Brands, Occasion


class CategorySerializer(serializers.ModelSerializer):
    subcates_count = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = "__all__"
        depth = 5

    def get_fields(self):
        """
        :return:
        """
        fields = super(CategorySerializer, self).get_fields()
        fields['subcates'] = CategorySerializer(many=True)
        return fields

    @staticmethod
    def get_subcates_count(obj):
        """
        :param obj:
        :return:
        """
        if obj.is_parent:
            return obj.children().count()
        return obj.subcates.count()


class ByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        depth = 5

    def get_fields(self):
        """
        :return:
        """
        fields = super(ByCategorySerializer, self).get_fields()
        fields['subcates'] = ByCategorySerializer(many=True)
        return fields

    articles = serializers.SerializerMethodField(method_name='get_articles', source="article")

    @staticmethod
    def get_articles(obj):  #To get the related articles
        """
        :param obj:
        :return:
        """
        return ProductSerializer(obj.child_article, many=True).data


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

    # category = CategorySerializer(many=False, read_only=True,)# source='category_set'
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


class ReviewReadSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(required=False, read_only=True)

    class Meta:
        model = Reviews
        fields = "__all__"
        # depth = 2
