from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from BackendApp.models import Users
from .serializers import UsersSerializer

@api_view(['GET'])
def getData(request):
    users = Users.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)

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
        return Response(request.data)
    else:
        return HttpResponseBadRequest(f"Bad credentials! {serializer}", status=404)