from rest_framework import status, generics, permissions
from rest_framework.response import Response
from . import models, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

@extend_schema(tags=["Account"], description='Login into an Account.')
class LoginView(TokenObtainPairView):
    serializer_class = serializers.LoginTokenSerializer

@extend_schema(tags=["Account"], description='Create an Account.')
class SignupApi(generics.CreateAPIView):
    serializer_class = serializers.SignupSerializer
    queryset = models.Account.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'detail': 'Account created successfully',
            'account': {'email': serializer.instance.email}
        }, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Account"], description='Update an Account.')
class UpdateAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UpdateAccountSerializer

    def patch(self, request):
        try:
            id_ = request.user.id
            if not id_:
                return Response({"error": "Username not found"}, status=status.HTTP_400_BAD_REQUEST)
            account = models.Account.objects.get(id=id_)
            if account.id == request.user.id:
                serializer = serializers.UpdateAccountSerializer(account, data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error:", "You don't have permission to update this account."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema(tags=["Account"], description='Change account password.')
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password1'])
            user.save()
            return Response({"success": "Password Updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)