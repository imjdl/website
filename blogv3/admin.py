from django.contrib import admin
from . import models
# from django.contrib.sessions.models import Session    # 可以管理session
# Register your models here.
admin.site.register(models.Type)
# admin.site.register(Session)


# 优化后台管理
class ArticleModel(admin.ModelAdmin):
    list_display = ("article_title", "article_auth", "article_date", "article_commentnum", "article_scannum",
                    "article_type")
    search_fields = ("article_title",)
    ordering = ("article_commentnum", "article_scannum")
    list_filter = ['article_date', 'article_type']  # 过滤器
    list_per_page = 5  # 分页


class CommentModel(admin.ModelAdmin):
    list_display = ("com_article", "com_type", "com_user", "com_ip", "com_date")
    search_fields = ("com_content",)


class StayMsgModel(admin.ModelAdmin):
    list_display = ("stay_user",  "stay_ip", "stay_date")
    search_fields = ("stay_content",)


class Usermodel(admin.ModelAdmin):
    list_display = ("login", "url", "name", "email", "blog")
    search_fields = ("name", "login",)


admin.site.register(models.Article, ArticleModel)
admin.site.register(models.Comment, CommentModel)
admin.site.register(models.StayMessage, StayMsgModel)
admin.site.register(models.User, Usermodel)
