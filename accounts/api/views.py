from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.api.serializers import UserCreationSerializer, UserSerializer, LoginSerializer
from rest_framework import viewsets
from rest_framework import generics, mixins
from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

class UserCreationView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserCreationSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class UserLoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            data = UserSerializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    

class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        token, created = Token.objects.get_or_create(user=request.user)
        data['token'] = token.key
        return Response(data, status=status.HTTP_200_OK)