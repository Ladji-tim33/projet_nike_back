from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response

from .models import Product, Category, Brand, Favorite
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, CartItemSerializer, FavoriteSerializer
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from rest_framework.exceptions import ValidationError


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Mettre ça ici (au niveau de la classe)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        brand_id = self.request.query_params.get('brand')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        return queryset

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # On ne retourne que les éléments du panier de l'utilisateur connecté
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # L'utilisateur connecté est automatiquement attaché
        serializer.save(user=self.request.user)  

class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product")

        if not product_id:
            raise ValidationError({"product": "Champ requis."})

        # Vérifie si ce favori existe déjà
        existing = Favorite.objects.filter(user=user, product_id=product_id).first()

        if existing:
            # Supprimer = toggle off
            existing.delete()
            return Response({"removed": True, "productId": int(product_id)}, status=status.HTTP_200_OK)

        # Ajouter = toggle on
        favorite = Favorite.objects.create(user=user, product_id=product_id)
        serializer = self.get_serializer(favorite)
        return Response({"removed": False, "favorite": serializer.data}, status=status.HTTP_201_CREATED)