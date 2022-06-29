from django.db import transaction
from rest_framework import serializers
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from users.serializers import UserCurrentSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Чтобы значение user автоматически подставлялось при создании категории,
    мы можем переопределить поле user
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategoryListSerializer(serializers.ModelSerializer):
    # TODO не будем менять пользователя в PUT
    # TODO разночтения со Swagger в PUT можно что менять пользователя категории? Зачем?
    user = UserCurrentSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя и скрыть
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # добавлено в соотвествии с Swagger
    due_date = serializers.DateField(format="%Y-%m-%d")

    # due_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    # Соединяемся по SlugField не добавляем метод get_or_create так в данной задаче
    # Мы выбираем только из существующих категорий.
    # category = serializers.SlugRelatedField(many=False,
    #                                         required=False,
    #                                         slug_field='id',
    #                                         queryset=GoalCategory.objects.all()
    #                                         )

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    # def validate_category(self, value):
    #     if value.is_deleted:
    #         raise serializers.ValidationError("not allowed in deleted category")
    #
    #     if value.user != self.context["request"].user:
    #         raise serializers.ValidationError("not owner of category")
    #
    #     return value


class GoalListSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя
    user = UserCurrentSerializer(read_only=True)
    due_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"


class GoalRUDASerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя
    user = UserCurrentSerializer(many=False, required=False, read_only=True)
    due_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    # Исходя из swagger user {} должен быть в put зачем-то, если только применять как кто последний редактировал
    # Тот и будет сохранен в User
    def is_valid(self, raise_exception=False):
        # Словарь который передает пользователь
        self._user = self.context["request"].user
        return super().is_valid(raise_exception=raise_exception)

    # изменение пользователя, вообще это неправильно,
    def update(self, instance, validated_data):
        """
        http://localhost:8000/goals/goal/4/
        {
            "user": {
                "username": "test@teamdev.ru" - необязательно
            },
            "due_date": "2022-06-26",
            "title": "Цель 1",
            "description": "Описание тестовой цели 1",
            "status": 1,
            "priority": 1,
            "category": 1
        }
        """
        with transaction.atomic():
            """
            instance = Goal object
            """
            # Способность менять пользователя.
            # print(User.objects.get(pk=self._user.get('username').id))

            # instance.user.last_name = self._user.get('last_name', instance.user.last_name)
            # User.objects.filter(username=self._user.get('username')).update(
            #     last_name=instance.user.last_name
            # )
            # Сохраняем, пользователя который последний раз редактировал цель
            instance.user = User.objects.get(username=self._user)
            #instance.user.username = self._user.username
            # instance.user.first_name = self._user.get('first_name', instance.user.first_name)
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.category = validated_data.get('category', instance.category)
            instance.status = validated_data.get('status', instance.status)
            instance.priority = validated_data.get('priority', instance.priority)
            instance.save()
        return instance


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя и скрыть
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Соединяемся по SlugField не добавляем метод get_or_create так в данной задаче
    # Мы выбираем только из существующих категорий.
    # goal = serializers.SlugRelatedField(many=False,
    #                                         required=False,
    #                                         slug_field='id',
    #                                         queryset=Goal.objects.all()
    #                                         )

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCommentListSerializer(serializers.ModelSerializer):
    # Позволяет поймать текущего пользователя
    # TODO разночтения со Swagger в PUT, меняем только текст, user не меняем!!!
    user = UserCurrentSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"


# Create
class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    # TODO BoardParticipantSerializer ставим required=False
    # Ну а представим что он не указал participants и шо такого?
    # Хочется title обновить, а без participants не сможет,
    # На кой спрашивается так делать?
    participants = BoardParticipantSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    # TODO намудрили итог все равно неверный, чел себя не сможет обновить,
    # так как у вас unique constraint, пришлось переделывать выше
    """
    participants": [
       { 
           "role": 1,
           "user": "test2@teamdev.ru"
       }
    ],
    """
    def update(self, instance, validated_data):
        if validated_data.get("participants"):
            # owner от кого получаем запрос.
            owner = validated_data.pop("user")
            new_participants = validated_data.pop("participants")
            # Добавлено owner.id != чтобы каким-то неведомым образом пользователь не указал самого себя
            new_by_id = {part["user"].id: part for part in new_participants if owner.id != part["user"].id}
            print('new_by_id', new_by_id)
            old_participants = instance.participants.exclude(user=owner)
            with transaction.atomic():
                for old_participant in old_participants:
                    if old_participant.user_id not in new_by_id:
                        old_participant.delete()
                    else:
                        if (
                                old_participant.role
                                != new_by_id[old_participant.user_id]["role"]
                        ):
                            old_participant.role = new_by_id[old_participant.user_id][
                                "role"
                            ]
                            old_participant.save()
                        new_by_id.pop(old_participant.user_id)
                for new_part in new_by_id.values():
                    BoardParticipant.objects.create(
                        board=instance, user=new_part["user"], role=new_part["role"]
                    )
                instance.title = validated_data["title"]
                instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
