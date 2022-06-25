from django.contrib import admin
from goals.models import Goal, GoalCategory, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "status")
    search_fields = ("title", "user", "status")
    list_filter = ('status',)


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "goal")
    search_fields = ("text", "goal")
    list_filter = ('goal',)


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("board", "user", "role")
    search_fields = ("board",)
    list_filter = ('board',)


class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "is_deleted")
    search_fields = ("title",)
    list_filter = ('is_deleted',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
admin.site.register(Board, BoardAdmin)
