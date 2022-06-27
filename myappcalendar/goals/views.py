from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from goals.filters import GoalDateFilter, GoalCommentFilter, GoalCategoryFilter
from goals.models import GoalCategory, Goal, Status, GoalComment, Board
from goals.permissions import BoardPermissions, GoalCatCreatePermissions, GoalCatRetrievePermissions, \
    GoalRetrievePermissions, GoalCommentCreatePermissions, GoalCommentRetrievePermissions, GoalCreatePermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategoryListSerializer, GoalCreateSerializer, \
    GoalListSerializer, \
    GoalCommentCreateSerializer, GoalCommentListSerializer, BoardSerializer, BoardCreateSerializer, BoardListSerializer, \
    GoalRUDASerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCatCreatePermissions]

    # def create(self, request, *args, **kwargs):
    #     request.data['user'] = request.user.id
    #     return super().create(request, *args, **kwargs)


class GoalCategoryListView(ListAPIView):
    queryset = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryListSerializer

    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalCategoryFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]

    # search_fields = ["=title"]

    # Фильтруем на текущего пользователя
    def get_queryset(self):
        # Сначала через внешний ключ идем в доски, потом через обратный запрос достаем, пользователя пользователь
        # должен видеть не только те категории, которые создал сам,
        # но и другие, в досках которых он является участником.
        # TODO возможно не совсем верно, но все же, я решил что если он является участником,
        # То не важно создатель он или нет.
        # Не увидел огромного преимущества от related
        return GoalCategory.objects.select_related('user').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryListSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCatRetrievePermissions]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            Q(board__participants__user=self.request.user, is_deleted=False)
        )

    # Для того, чтобы категория не удалялась, при вызове delete, категория удаленные
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalCreatePermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter

    @extend_schema(
        description="Retrieve goal list",
        summary="goal list",
        parameters=[
            OpenApiParameter(name='due_date__lte', description='Filter by due_date less than', required=False,
                             type=str),
            OpenApiParameter(name='due_date__gte', description='Filter by due_date greater than', required=False,
                             type=str),
            OpenApiParameter(name='category', description='Filter by name of category',
                             required=False, type=int),
            OpenApiParameter(name='category__in', description='Filter by name category__in',
                             required=False, type=str),
            OpenApiParameter(name='priority', description='Filter by name of priority',
                             required=False, type=int),
            OpenApiParameter(name='priority__in', description='Filter by name priority__in',
                             required=False, type=int),
            OpenApiParameter(name='category__board', description='Filter by board if category in value',
                             required=False, type=int),
            OpenApiParameter(name='status', description='Filter by status', required=False,
                             type=int),
            OpenApiParameter(name='priority', description='Filter by priority', required=False,
                             type=int),
            OpenApiParameter(name='title', description='Filter by title', required=False,
                             type=str)]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    pagination_class = LimitOffsetPagination
    ordering_fields = ["title", "created"]
    ordering = ["created"]

    # Пользователю выдаются только те цели, которые находятся в категориях,
    # в досках которых он является участником.
    def get_queryset(self):
        return Goal.objects.filter(
            Q(category__board__participants__user=self.request.user)
        )


class GoalRUDAView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalRUDASerializer
    permission_classes = [permissions.IsAuthenticated, GoalRetrievePermissions]

    # Пользователю выдаются только те цели, которые находятся в категориях,
    # в досках которых он является участником.
    def get_queryset(self):
        return Goal.objects.filter(
            Q(category__board__participants__user=self.request.user)
        )

    # Добавляем в архив
    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, GoalCommentCreatePermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentListSerializer

    #
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalCommentFilter
    # search_fields = ["=goal__id"]
    filterset_fields = ['goal']
    # С этим дерьмом не работает.&search=%5Bobject%20Object%5D& search_fields
    pagination_class = LimitOffsetPagination
    ordering_fields = ["created"]
    ordering = ["-created"]

    # Пользователю выдаются только те комментарии, которые находятся в целях,
    # в досках которых он является участником.
    def get_queryset(self):
        return GoalComment.objects.filter(
            Q(goal__category__board__participants__user=self.request.user)
        )


class GoalCommenRUDAView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentListSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentRetrievePermissions]

    # Пользователю выдаются только те комментарии, которые находятся в целях,
    # в досках которых он является участником.

    def get_queryset(self):
        return GoalComment.objects.filter(
            Q(goal__category__board__participants__user=self.request.user)
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        # INNER JOIN boardparticipant ON (board.id = boardparticipant.board_id)
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Status.archived
            )
        return instance


class BoardCreateView(CreateAPIView):
    """
    is_deleted - указывать необязательно
    Post
    {
        "title": "Test board",
        "is_deleted": false
    }
    response
    {
    "id": int,
    "created": "2022-06-21T12:51:40.752242+03:00",
    "updated": "2022-06-21T12:51:40.752242+03:00",
    "title": "Test board",
    "is_deleted": false
    }
    """
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    """
    response
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "created": "2022-06-21T09:56:43.140Z",
                "updated": "2022-06-21T09:56:43.140Z",
                "title": "string",
                "is_deleted": true
            }
        ]
    }"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer

    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["title"]
    ordering = ["title"]

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        # select_related() doesn't works for backwards foreignkey relations.
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
