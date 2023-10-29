from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer

from api.permissions import IsAuthorOrHiAccessOrReadOnly
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrHiAccessOrReadOnly]

    def get_queryset(self):
        title_id = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        review_queryset = Review.objects.filter(title_id=title_id)
        return review_queryset

    def perform_create(self, serializer):
        title_id = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrHiAccessOrReadOnly]

    def get_queryset(self):
        review_id = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        comment_queryset = Comment.objects.filter(review_id=review_id)
        return comment_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review_id=review)
