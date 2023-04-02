from api import serializers
from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminModeratorAuthorOrReadOnly,
                             IsAdminOrReadOnly)
from api.utils import CategoryGenreViewSet
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User


class SignUpView(generics.CreateAPIView):
    """Самостоятельная регистрация новых пользователей.
    Получение confirmation_code на электронную почту пользователя."""
    queryset = User.objects.all()
    serializer_class = serializers.SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers,
                        )

    def perform_create(self, serializer):
        """Действие."""
        new_user = serializer.save()
        unique_code = default_token_generator.make_token(new_user)
        serializer.save(confirmation_code=unique_code)
        new_user.email_user(
            subject='Подтверждение регистрации.',
            message=f'Код: {unique_code}!'
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение пользователем токена для авторизации."""
    serializer = serializers.TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(user)
    return Response({f'token: {token}'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Работа админа с пользователями.
    Авторизованный пользователь может редактировать свой профиль."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ['username']

    @action(
        detail=False,
        methods=(['GET', 'PATCH']),
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = serializers.UserSerializer(request.user)
            return Response(serializer.data)

        serializer = serializers.UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    """Реализация CRUD для модели Title."""
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.GetTitleSerializer
        return self.serializer_class


class CategoryViewSet(CategoryGenreViewSet):
    """Реализация CRUD для модели Category."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Реализация CRUD для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Описание действий для модели Review."""
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_post(self):
        """Отправить или получить запись."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получение информации о записи."""
        return self.get_post().reviews.all()

    def perform_create(self, serializer):
        """Действие."""
        serializer.save(author=self.request.user, title=self.get_post())


class CommentViewSet(viewsets.ModelViewSet):
    """Описание действий для модели Comment."""
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_post(self):
        """Отправить или получить запись."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получение информации о записи."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Действие."""
        serializer.save(author=self.request.user, review=self.get_post())
