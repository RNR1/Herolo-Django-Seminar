from main.views import AuthorViewSet, BookViewSet, TagViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('authors', AuthorViewSet, basename='authors')
router.register('books', BookViewSet, basename='books')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = router.urls
