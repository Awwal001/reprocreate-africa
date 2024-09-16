# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from .models import Product, Category
# from central.models import School
# from .serializers import ProductSerializer, CategorySerializer


# @api_view(['GET'])
# def getProducts(request):
#     query = request.query_params.get('keyword')
#     if query == None:
#         query = ''

#     products = Product.objects.filter(
#         title__icontains=query).order_by('-created_at')

#     page = request.query_params.get('page')
#     paginator = Paginator(products, 10)

#     try:
#         products = paginator.page(page)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)

#     if page == None:
#         page = 1

#     page = int(page)
#     print('Page:', page)
#     serializer = ProductSerializer(products, many=True)
#     return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


# @api_view(['GET'])
# def getproductsByCategory(request, pk):
#     category = Category.objects.get(id=pk)
#     products = category.product_set.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# # @api_view(['GET'])
# # def getTopproducts(request):
# #     products = product.objects.filter(rating__gte=4).order_by('-rating')[0:7]
# #     serializer = productSerializer(products, many=True)
# #     return Response(serializer.data)

# @api_view(['GET'])

# def getAdminProducts(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def getProduct(request, pk):
#     product = Product.objects.get(id=pk)
#     serializer = ProductSerializer(product, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def createProduct(request):
#     user = request.user
#     data = request.data
#     cat_id = data['category']
#     category = Category.objects.get(id=cat_id)
#     sch_id = data['school']
#     school = School.objects.get(id=sch_id)

#     product = product.objects.create(
#         realtor=user,
#         title='',
#         description='',
#         location='',
#         price=0,
#         agent_fee=0,
#         category=category,
#         number_of_rooms=0,
#         gated_compound=False,
#         running_water=False,
#         generator=False,
#         new_house=False,
#         state='',
#         school=school
#     )

#     serializer = ProductSerializer(product, many=False)
#     return Response(serializer.data)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateProduct(request, pk):
#     data = request.data
#     product = product.objects.get(id=pk)
#     cat_id = data['category']
#     category = Category.objects.get(id=cat_id)
    

#     product.title = data['title']
#     product.price = data['price']
#     product.description = data['description']
#     product.location = data['location']
#     product.category = category
#     product.agent_fee = data['agent_fee']
#     product.number_of_rooms = data['number_of_rooms']
#     product.gated_compound = data['gated_compound']
#     product.running_water = data['running_water']
#     product.generator = data['generator']
#     product.new_house = data['new_house']
#     product.state = data['state']
#     product.school = data['school']

#     product.save()

#     serializer = ProductSerializer(product, many=False)
#     return Response(serializer.data)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def deleteProduct(request, pk):
#     product = Product.objects.get(id=pk)
#     product.delete()
#     return Response('product Deleted')


# @api_view(['POST'])
# def uploadImage(request):
#     data = request.data

#     productid = data['productid']
#     product = Product.objects.get(id=productid)

#     product.image = request.FILES.get('image')
#     product.save()

#     return Response('Image was uploaded')



# @api_view(['GET'])
# def getCategories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getCategory(request, pk):
#     category = Category.objects.get(id=pk)
#     serializer = CategorySerializer(category, many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def createCategory(request):
#     user = request.user
#     data = request.data

#     category = Category.objects.create(
#         user=user,
#         name=data['name'],
#     )

#     serializer = CategorySerializer(category, many=False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def updateCategory(request, pk):
#     data = request.data
#     category = Category.objects.get(id=pk)

#     category.name = data['name']

#     category.save()

#     serializer = CategorySerializer(category, many=False)
#     return Response(serializer.data)


# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def deleteCategory(request, pk):
#     category = Category.objects.get(id=pk)
#     category.delete()
#     return Response('Category Deleted')
    