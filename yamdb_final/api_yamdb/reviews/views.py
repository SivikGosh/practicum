from api.permissions import IsAuthorOrHiAccessOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from titles.models import Title

from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrHiAccessOrReadOnly]

    def get_queryset(self):
        title_id = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return Review.objects.filter(title_id=title_id)

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
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review_id=review)
