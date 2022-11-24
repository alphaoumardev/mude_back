from rest_framework import serializers

from mart.models import Categories, Tag, Materials, Product, ColorsOption, Lengths, SizesOption, Reviews


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'


class ColorsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorsOption
        fields = '__all__'


class LengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lengths
        fields = '__all__'


class SizeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SizesOption
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
