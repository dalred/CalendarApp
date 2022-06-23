from django.db import models
from django_filters import rest_framework as filters
from goals.models import Goal, GoalComment, GoalCategory


# https://django-filter.readthedocs.io/en/stable/guide/usage.html
from users.models import User


class GoalDateFilter(filters.FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
            "title": ("exact", "in", "icontains"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": filters.IsoDateTimeFilter},
    }


class GoalCommentFilter(filters.FilterSet):
    # Сделано так потому что пришлось бы fields = { "goal__id": ["exact"]}
    # Field names can traverse relationships by joining the related parts with the ORM lookup separator (__)
    goal = filters.filters.ModelChoiceFilter(queryset=Goal.objects.all())

    class Meta:
        model = GoalComment
        # means exact ?goal=...
        fields = ["goal"]


class GoalCategoryFilter(filters.FilterSet):
    # Применяется во основном для many связей
    user = filters.filters.ModelMultipleChoiceFilter(field_name='user__username',
                                                  queryset=User.objects.all(),
                                                  lookup_expr="exact",
                                                  to_field_name='username', )


    class Meta:
        model = GoalCategory
        fields = ['user', 'board']