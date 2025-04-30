from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserListSerializer
from rest_framework.permissions import AllowAny   
from django.contrib.auth.models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(f"Request Data: {request.data}")  # Zum Debuggen
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        print(f"Errors: {serializer.errors}")  # Fehlerausgabe in der Konsole
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    permission_classes = [AllowAny]  # Sicherstellen, dass der Benutzer authentifiziert ist

    def get(self, request):
        users = User.objects.all()  # Alle Benutzer abrufen
        serializer = UserListSerializer(users, many=True)  # Viele Benutzer serialisieren
        return Response(serializer.data, status=status.HTTP_200_OK)    