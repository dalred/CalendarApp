from django.db.models import Q
from rest_framework import permissions

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCatCreatePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        board = request.data.get('board')
        if not board:
            raise permissions.exceptions.APIException("field board is required!")
        # В случае если пользователю нужно быть участником или владельцем или модератором доски,
        # чтобы создать категорию
        return BoardParticipant.objects.filter(
            Q(user=request.user) &
            Q(board=board) &
            (Q(role=BoardParticipant.Role.writer) | Q(
                role=BoardParticipant.Role.owner))
        ).exists()


class GoalCatRetrievePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        """
        RUDA
        {
          "title": "string",
          "is_deleted": false
        }
        """
        # board не указываем потому что одна категория может быть только в одном борде, а не в нескольких
        return GoalCategory.objects.filter(
            (Q(board__participants__user=request.user) &
             Q(board__participants__role=BoardParticipant.Role.owner) |
             Q(board__participants__role=BoardParticipant.Role.writer)) &
            Q(id=obj.id, is_deleted=False)).exists()


class GoalCreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        category_id = request.data.get('category')
        if not category_id:
            raise permissions.exceptions.APIException("field category is required!")
        # В случае если пользователю нужно быть участником или владельцем или модератором доски,
        # чтобы создать категорию
        return GoalCategory.objects.filter(
            Q(board__participants__user=request.user) &
            Q(id=category_id) &
            Q(board__participants__role=BoardParticipant.Role.owner) |
            Q(board__participants__role=BoardParticipant.Role.writer)
        ).exists()


class GoalRetrievePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        """
        Put
        {
            "title": "Цель 21",
            "due_date": "2022-06-25T12:29:44.056780+03:00",
            "description": "Описание тестовой цели",
            "status": 2,
            "priority": 1,
            "category": 21
        }
        Q(category__board__participants__user=self.request.user)
            """
        return Goal.objects.filter(
            (Q(category__board__participants__role=BoardParticipant.Role.owner) |
             Q(category__board__participants__role=BoardParticipant.Role.writer)) &
            Q(category__board__participants__user=request.user) &
            Q(id=obj.id)).exists()


class GoalCommentCreatePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        goal = request.data.get('goal')
        if not goal:
            raise permissions.exceptions.APIException("field goal is required!")
        # В случае если пользователю нужно быть владельцем или модератором доски,
        # чтобы создать Comment
        return Goal.objects.filter(
            (Q(category__board__participants__role=BoardParticipant.Role.owner) |
             Q(category__board__participants__role=BoardParticipant.Role.writer)) &
            Q(category__board__participants__user=request.user) &
            Q(id=goal)).exists()


# RUDA
# Пользователь всё так же не может редактировать/удалять чужие комментарии.
class GoalCommentRetrievePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        """
        RUDA
        {
            "user": {
            "username": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com"
            },
            "text": "string"
        }
        """
        return GoalComment.objects.filter(Q(user=request.user) &
                                          Q(id=obj.id)).exists()
