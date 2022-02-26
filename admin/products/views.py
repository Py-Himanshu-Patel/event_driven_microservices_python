from random import choice
from flask import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, User
from .serializers import ProductSerializer
from rest_framework.views import APIView


class ProductViewSet(viewsets.ViewSet):
	def list(self, request):
		products = Product.objects.all()
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)

	def create(self, request):
		serializer = ProductSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk=None):
		product = Product.objects.filter(id=pk)
		if not product.exists():
			return Response({},status=status.HTTP_404_NOT_FOUND)
		product = product.first()
		serializer = ProductSerializer(product)
		return Response(serializer.data)
		

	def update(self, request, pk=None):
		product = Product.objects.filter(id=pk)
		if not product.exists():
			return Response({},status=status.HTTP_404_NOT_FOUND)
		serializer = ProductSerializer(instance=product, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

	def destroy(self, request, pk=None):
		product = Product.objects.filter(id=pk)
		if not product.exists():
			return Response({},status=status.HTTP_404_NOT_FOUND)
		product = product.first()
		product.delete()
		return Response({"delete_product": pk}, status=status.HTTP_204_NO_CONTENT)		


class UserAPIView(APIView):
	def get(self, _):
		users = User.objects.all()
		user = choice(users)
		return Response({
			'id': user.id
		})
