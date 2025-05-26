from rest_framework import serializers
from .models import Category, Brand, Product, Favorite
from .models import CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    # Afficher le nom de la catégorie et de la marque dans le JSON
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    # Pour envoyer les IDs en écriture (POST/PUT)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source='brand', write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image', 'stock',
            'category', 'brand', 'category_id', 'brand_id', 'created_at'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product_data = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'quantity', 'added_at', 'product_data']
        read_only_fields = ['user', 'added_at']
        

class FavoriteSerializer(serializers.ModelSerializer):
    product_data = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_data', 'created_at']
        read_only_fields = ['user', 'created_at']
