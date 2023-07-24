from api.permissions import IsAdminOrReadOnly
from rest_framework import mixins, serializers, viewsets
from rest_framework.filters import SearchFilter


class GenreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'slug'


class ReviewCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )


class CategoryGenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
