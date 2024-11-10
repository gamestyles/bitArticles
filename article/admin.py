from django.contrib import admin

from .models import Article, ArticleScore


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    readonly_fields = ("created_at", )


class ArticleScoreAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user_id", "score", "created_at", "is_suspicious")
    list_select_related = ("article", )
    readonly_fields = ("created_at", )


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleScore, ArticleScoreAdmin)
