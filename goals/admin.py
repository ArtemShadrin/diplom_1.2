from django.contrib import admin

from goals.models import GoalComment, Goal, GoalCategory, Board, BoardParticipant


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_deleted')
    readonly_fields = ('created', 'updated')
    list_filter = ('is_deleted',)
    search_fields = ('title',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category')
    readonly_fields = ('created', 'updated')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'text')
    readonly_fields = ('created', 'updated')
    search_fields = ('text', 'user')


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted')


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')
