import django_filters
from django.db import models
from django_filters import rest_framework
from goals.models import Goal, GoalComment


# https://django-filter.readthedocs.io/en/stable/guide/usage.html

class GoalDateFilter(rest_framework.FilterSet):
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
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }


class GoalCommentFilter(rest_framework.FilterSet):
    # Сделано так потому что пришлось бы fields = { "goal__id": ["exact"]}
    # Field names can traverse relationships by joining the related parts with the ORM lookup separator (__)
    goal = django_filters.filters.ModelChoiceFilter(queryset=Goal.objects.all())

    class Meta:
        model = GoalComment
        # means exact ?goal=...
        fields = ["goal"]
