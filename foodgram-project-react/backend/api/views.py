from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import FILE_NAME
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscribe, User

from .filters import RecipeFilter
from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag
from .pagination import CustomPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, RecipeSerializer,
                          SetPasswordSerializer, SubscribeAuthorSerializer,
                          SubscriptionsSerializer, TagSerializer,
                          UserCreateSerializer, UserReadSerializer)


class GetModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(GetModelViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserReadSerializer
        return UserCreateSerializer

    @action(detail=False, methods=['get'], pagination_class=None,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {'detail': 'Пароль успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated],
            pagination_class=CustomPaginator)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = SubscribeAuthorSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(
                Subscribe, user=request.user, author=author
            ).delete()
            return Response(
                {'detail': 'Успешная отписка'},
                status=status.HTTP_204_NO_CONTENT
            )


class TagViewSet(GetModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(GetModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = (
        Recipe.objects
        .select_related('author')
        .prefetch_related('ingredients', 'tags')
        .all()
    )
    pagination_class = CustomPaginator
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'create', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = RecipeSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not Favorite.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'DELETE':
            get_object_or_404(
                Favorite, user=request.user, recipe=recipe
            ).delete()
            return Response(
                {'detail': 'Рецепт успешно удален из избранного.'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,), pagination_class=None)
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = RecipeSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not Cart.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                Cart.objects.create(user=request.user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'DELETE':
            get_object_or_404(Cart, user=request.user, recipe=recipe).delete()
            return Response(
                {'detail': 'Рецепт успешно удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_recipe__user=request.user
            ).values('ingredient').annotate(
                total_amount=Sum('amount')
            ).values_list(
                'ingredient__name',
                'total_amount',
                'ingredient__measurement_unit'
            )
        )

        file_list = []
        for ingredient in ingredients:
            file_list.append('{} - {} {}.'.format(*ingredient))

        file = HttpResponse(
            'Cписок покупок:\n' + '\n'.join(file_list),
            content_type='text/plain'
        )
        file['Content-Disposition'] = (f'attachment; filename={FILE_NAME}')

        return file