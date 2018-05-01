from django.db import models

# Create your models here.


class Type(models.Model):
    type_id = models.AutoField(primary_key=True, null=False)
    type_content = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.type_content


class Article(models.Model):
    article_id = models.AutoField(primary_key=True, null=False, verbose_name="文章id")
    article_title = models.CharField(max_length=100, verbose_name="标题")
    article_auth = models.CharField(default='elloit', max_length=64, null=False, verbose_name="作者")
    article_date = models.DateField(null=False, verbose_name="发布日期")
    article_commentnum = models.IntegerField(default=0, null=False, verbose_name="评论数")
    article_scannum = models.IntegerField(default=0, null=False, verbose_name="浏览量")
    article_content = models.TextField(null=False)
    article_type = models.ForeignKey(to=Type, on_delete=models.CASCADE, verbose_name="类型")

    def __str__(self):
        return self.article_title


class User(models.Model):
    id = models.IntegerField(primary_key=True)  # github用户ID
    login = models.CharField(max_length=100, verbose_name="github登录名")    # github 登录名
    avatar_url = models.URLField()  # 头像
    url = models.URLField(verbose_name="主页地址")     # GitHub 主页
    name = models.CharField(max_length=100, verbose_name="用户名")     # 用户名
    email = models.EmailField(null=True, verbose_name="email")     # email
    blog = models.URLField(null=True, verbose_name="blog")       # blog

    def __str__(self):
        return self.login


class Comment(models.Model):
    com_id = models.AutoField(primary_key=True, null=False)
    com_article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")
    com_type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="类型")
    com_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论者")
    com_content = models.TextField(null=False, verbose_name="内容")
    com_ip = models.CharField(max_length=15, verbose_name="IP")
    com_date = models.DateTimeField(null=False, verbose_name="时间")

    def __str__(self):
        return str(self.com_content)


class StayMessage(models.Model):
    stay_id = models.AutoField(primary_key=True, null=False)
    stay_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="留言者")
    stay_content = models.TextField(null=False, verbose_name="留言内容")
    stay_ip = models.CharField(max_length=15, verbose_name="IP")
    stay_date = models.DateTimeField(null=False, verbose_name="时间")

    def __str__(self):
        return self.stay_content
