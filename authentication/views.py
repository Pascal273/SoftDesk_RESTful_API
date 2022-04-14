from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authentication.serializers import UserSerializer, SignUpSerializer
from .permissions import IsNotAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    User = get_user_model()
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserSignUpView(GenericAPIView):
    """
    API endpoint that allows not new users to signup.
    """
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny, IsNotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(serializer.data['email'],
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
