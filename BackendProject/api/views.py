from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.decorators import api_view
from BackendApp.models import Users, Product, PurchaseHistory
from .serializers import UsersSerializer, ProductSerializer, PurchaseHistorySerializer
from django.contrib.auth import authenticate

@api_view(['GET'])
def getData(request):
    users = Users.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserById(request, pk):
    try:
        user = Users.objects.get(pk=pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    except Users.DoesNotExist:
        return HttpResponseNotFound("Пользователь не найден")
    
@api_view(['GET'])
def getUserByUsernamePassword(request):
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'message': 'User found', 'username': user.username}, status=200)
    else:
        return Response({'message': 'Invalid credentials'}, status=404)

@api_view(['POST'])
def addUsers(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return HttpResponseBadRequest(
            f"Bad credentials! {serializer}",
            status=404)


@api_view(['GET'])
def getAllProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Получение данных о конкретном продукте по ID
@api_view(['GET'])
def getProductById(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Продукт не найден")

# Получение истории покупок конкретного клиента
@api_view(['GET'])
def getPurchaseHistoryByClient(request, client_id):
    purchases = PurchaseHistory.objects.filter(client_id=client_id)
    serializer = PurchaseHistorySerializer(purchases, many=True)
    return Response(serializer.data)

# Обновление данных пользователя
@api_view(['PUT'])
def updateUser(request, pk):
    try:
        user = Users.objects.get(pk=pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    except Users.DoesNotExist:
        return HttpResponseNotFound("Пользователь не найден")

# Удаление пользователя
@api_view(['DELETE'])
def deleteUser(request, pk):
    try:
        user = Users.objects.get(pk=pk)
        user.delete()
        return Response(status=204)
    except Users.DoesNotExist:
        return HttpResponseNotFound("Пользователь не найден")

# Получение списка товаров по части названия
@api_view(['GET'])
def getProductsByName(request, name):
    products = Product.objects.filter(product_name__icontains=name)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Получение списка товаров с количеством больше определенного числа
@api_view(['GET'])
def getProductsByQuantity(request, quantity):
    products = Product.objects.filter(quantity__gte=quantity)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Получение списка товаров с рейтингом выше определенного значения
@api_view(['GET'])
def getProductsByRating(request, rating):
    products = Product.objects.filter(average_rating__gte=rating)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Получение списка покупок, которые еще не были оплачены
@api_view(['GET'])
def getUnpaidPurchases(request):
    purchases = PurchaseHistory.objects.filter(paid=False)
    serializer = PurchaseHistorySerializer(purchases, many=True)
    return Response(serializer.data)

# Получение списка всех покупок за определенный период
@api_view(['GET'])
def getPurchasesByDate(request, start_date, end_date):
    purchases = PurchaseHistory.objects.filter(
        created__range=[start_date, end_date]
    )
    serializer = PurchaseHistorySerializer(purchases, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addProduct(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return HttpResponseBadRequest(
            f"Неверные данные {serializer}",
            status=404)

@api_view(['DELETE'])
def deleteProduct(request, pk):
    print(pk)
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=204)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Продукт не найден")
    
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')   
    try:
        user = Users.objects.get(username=username, password=password)
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    except Users.DoesNotExist:
        return Response({"message": "Invalid credentials"}, status=400)
    
@api_view(['GET'])
def getProductsByVendor(request, vendor):
    products = Product.objects.filter(vendor=vendor)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPurchaseHistoryByClient(request, client):
    products = PurchaseHistory.objects.filter(client=client)
    serializer = PurchaseHistorySerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def buyProduct(request):
    serializer = PurchaseHistorySerializer(data=request.data)
    if serializer.is_valid():
        client = serializer.validated_data['client']
        product = serializer.validated_data['product']

        # Delete any existing records with paid = False for the same client and product
        PurchaseHistory.objects.filter(client=client, product=product, paid=False).delete()

        # Create a new PurchaseHistory instance with 'paid' set to True
        serializer.validated_data['paid'] = True
        purchase_history = PurchaseHistory.objects.create(**serializer.validated_data)
        
        # Return the created instance data
        created_serializer = PurchaseHistorySerializer(purchase_history)
        return Response(created_serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
def addToShoppingCart(request):
    serializer = PurchaseHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return HttpResponseBadRequest(
            f"Неверные данные {serializer}",
            status=404)