from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, GenreViewSet, ConditionViewSet, BookViewSet, BookDetailView, UserBookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'conditions', ConditionViewSet, basename='condition')
router.register(r'books', BookViewSet, basename='books')
router.register(r'user-books', UserBookViewSet, basename='user-books')

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:pk>', BookDetailView.as_view(), name="book-detail"),
]

urlpatterns += [
    path('books/<int:pk>/offer-book/', BookViewSet.as_view({'post': 'offer_book'}), name='offer-book'),
    path('books/<int:pk>/take-book/', BookViewSet.as_view({'get': 'take_book'}), name='take-book'),
    path('books/<int:pk>/choose-recipient/', BookViewSet.as_view({'post': 'choose_recipient'}), name='choose-recipient')
]







