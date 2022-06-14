from rest_framework import serializers
from goals.models import GoalCategory, Goal, GoalComment
from users.serializers import UserCurrentSerializer


class GoalCatCreateSerializer(serializers.ModelSerializer):
    """
    Чтобы значение user автоматически подставлялось при создании категории,
    мы можем переопределить поле user
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserCurrentSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя и скрыть
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Соединяемся по SlugField не добавляем метод get_or_create так в данной задаче
    # Мы выбираем только из существующих категорий.
    category = serializers.SlugRelatedField(many=False,
                                            required=False,
                                            slug_field='id',
                                            queryset=GoalCategory.objects.all()
                                            )

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value


class GoalListSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя
    user = UserCurrentSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя и скрыть
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Соединяемся по SlugField не добавляем метод get_or_create так в данной задаче
    # Мы выбираем только из существующих категорий.
    goal = serializers.SlugRelatedField(many=False,
                                            required=False,
                                            slug_field='id',
                                            queryset=Goal.objects.all()
                                            )

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

class GoalCommentListSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя
    user = UserCurrentSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"