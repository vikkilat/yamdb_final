from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles', views.TitleViewSet)
router_v1.register(r'genres', views.GenreViewSet)
router_v1.register(r'categories', views.CategoryViewSet)
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/auth/token/', views.get_token, name='token'),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='sign_up'),
    path('v1/', include(router_v1.urls)),
]
