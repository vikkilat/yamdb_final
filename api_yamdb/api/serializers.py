from api import utils
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

REGEX = r"^[\w.@+-]+\Z"


class CategorySerializer(utils.GenreCategorySerializer):
    """Сериализатор модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(utils.GenreCategorySerializer):
    """Сериализатор модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title, кроме GET запросов."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        """Получение рейтинга."""
        rating = obj.reviews.aggregate(Avg('score', default=0))
        return rating.get('score__avg')


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор GET запросов к модели Title."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        """Получение рейтинга."""
        rating = obj.reviews.aggregate(Avg('score', default=0))
        return rating.get('score__avg')


class ReviewSerializer(utils.ReviewCommentSerializer):
    """Сериализатор для модели Review."""
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data):
        """Проверка один автор - одна оценка."""
        author = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        if self.context['request'].method != 'PATCH':
            if Review.objects.filter(
                    author=author,
                    title=title,
            ).exists():
                raise serializers.ValidationError(
                    'Можно поставить только одну оценку!'
                )

        return data

    def validate_score(self, value):
        """Проверка, что оценка - от 1 до 10 (целое число)."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка только в диапазоне от 1 до 10 (целое число)!'
            )
        return value


class CommentSerializer(utils.ReviewCommentSerializer):
    """Сериализатор для модели Comment."""
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Пользователь."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ProfileEditSerializer(serializers.ModelSerializer):
    """Сериализатор Редактирование профиля."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор Регистрация."""
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        REGEX,
        required=True,
        max_length=150,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """Создание профиля."""
        username = data.get('username')
        email = data.get('email')
        if (
                User.objects.filter(username=username).exists()
                and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError('username занят')
        if (
                User.objects.filter(email=email).exists()
                and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError('email занят')
        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Использование имени {value} '
                f'в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для работы с токеном."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100)
