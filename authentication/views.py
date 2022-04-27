from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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
    Only passwords which correspond to the validity assignments are accepted.
    """
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny, IsNotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                user = get_user_model()
                validate_password(serializer.data['password'], user)
            except ValidationError as error:
                return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

            serializer.create(serializer.data)
            return Response({'Account created': serializer.data['email']},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
