from django.contrib import admin
from goals.models import Goal, GoalCategory, GoalComment

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


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)