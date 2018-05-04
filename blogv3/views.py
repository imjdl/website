from django.shortcuts import render
from django.http import HttpResponse
from markdown import markdown
from django.http import JsonResponse
from threading import Thread
from django.conf import settings
from django import template
# Create your views here.
register = template.Library()


def index(request):
    from .models import Article
    articles = Article.objects.all()
    # 分页
    from django.core.paginator import Paginator
    # 一页显示文章数
    artnms = 5
    page = request.GET.get("p", 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    articles_page = articles.order_by('article_id')
    pages = Paginator(articles_page,  artnms)
    if page > pages.num_pages:
        page = pages.num_pages
    if page < 1:
        page = 1
    try:
        articles_page = pages.page(page)
    except NameError:
        articles_page = pages.page(1)

    # 读取最新的篇
    if page == 1:
        arts = articles.order_by('-article_id')[:page * artnms]
    else:
        arts = articles.order_by('-article_id')[(page - 1) * artnms:page * artnms]
    for art in arts:
        art.article_content = markdown(art.article_content, extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.abbr",
            "markdown.extensions.attr_list",
            "markdown.extensions.def_list",
            "markdown.extensions.fenced_code",
            "markdown.extensions.footnotes",
            "markdown.extensions.tables",
            "markdown.extensions.smart_strong",
            "markdown.extensions.admonition",
            "markdown.extensions.codehilite",
            "markdown.extensions.headerid",
            "markdown.extensions.meta",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
            "markdown.extensions.smarty",
            "markdown.extensions.toc",
            "markdown.extensions.wikilinks"])
    # 读取标签
    types = gettypes()
    # 热门文章(浏览量)
    hotarts = articles.order_by('-article_scannum')[:5]
    colors = ["btn-primary", "btn-info", "btn-success", "btn-danger", "btn-warning", "btn-rose"]
    sizes = ["btn-sm", "btn-lg", ""]
    return render(request, 'blogv3/index.html', context={'arts': arts, 'types': types, 'hotarts': hotarts, 'articles_page': articles_page, 'pages': getpages(pages.num_pages, page), 'year_month_number': getarching(), "colors": colors, "sizes": sizes})


def article(request, pk):
    try:
        pk = int(pk)
    except ValueError:
        return HttpResponse('数据错误')

    # 读取指定id文章
    from .models import Article
    try:
        art = Article.objects.get(article_id=pk)
        art.article_scannum += 1
        art.save()
        art.article_content = markdown(art.article_content, extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.abbr",
            "markdown.extensions.attr_list",
            "markdown.extensions.def_list",
            "markdown.extensions.fenced_code",
            "markdown.extensions.footnotes",
            "markdown.extensions.tables",
            "markdown.extensions.smart_strong",
            "markdown.extensions.admonition",
            "markdown.extensions.codehilite",
            "markdown.extensions.headerid",
            "markdown.extensions.meta",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
            "markdown.extensions.smarty",
            "markdown.extensions.toc",
            "markdown.extensions.wikilinks"])
    except Article.DoesNotExist:
        art = []
    # 获取标签
    # types = gettypes()
    # # 获取热门
    # hotarts = Article.objects.all().order_by('-article_scannum')[:5]
    islogin = request.session.get('islogin', None)
    username = request.session.get('username', None)
    avatar_url = request.session.get('avatar_url', None)

    # 获取评论
    coms = []
    if art != []:
        coms = getcoments(art)

    return render(request, 'blogv3/html/article.html',
                  context={'art': art, 'islogin': islogin, 'username': username,
                           'avatar_url': avatar_url, 'coms': coms})


def about(request):

    return render(request, 'blogv3/html/about.html')


def captcha(request):
    return HttpResponse(code(request))


def timeline(request):
    from .models import Article
    dates = Article.objects.dates('article_date', 'day', order='DESC')
    articles = Article.objects.values('article_id', 'article_title', 'article_date')
    return render(request, 'blogv3/html/timeline.html', context={'articles': articles, 'dates': dates})


def search(request):
    from .models import Article
    word = request.GET.get('word', '')
    if word == "":
        arts = []
    else:
        arts = Article.objects.filter(article_title__contains=word) | Article.objects.filter(article_content__contains=word)
        for art in arts:
            art.article_content = markdown(art.article_content, extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.abbr",
                "markdown.extensions.attr_list",
                "markdown.extensions.def_list",
                "markdown.extensions.fenced_code",
                "markdown.extensions.footnotes",
                "markdown.extensions.tables",
                "markdown.extensions.smart_strong",
                "markdown.extensions.admonition",
                "markdown.extensions.codehilite",
                "markdown.extensions.headerid",
                "markdown.extensions.meta",
                "markdown.extensions.nl2br",
                "markdown.extensions.sane_lists",
                "markdown.extensions.smarty",
                "markdown.extensions.toc",
                "markdown.extensions.wikilinks"])
    return render(request, "blogv3/html/search.html", context={"arts": arts, 'word': word})


def login(request):

    import requests, json
    from config.config import headers
    from .models import User

    code = request.GET.get('code')
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    redirect_uri = settings.REDIRECT_URI
    re = requests.get("https://github.com/login/oauth/access_token?client_id="+client_id + "&client_secret=" +
                      client_secret+ "&code="+code + "&redirect_uri=" + redirect_uri, headers=headers)
    re = requests.get("https://api.github.com/user?" + re.text, headers=headers)
    res = json.loads(re.text)
    try:
        user = User.objects.get(id=res['id'])
        user.name = res['name']
        user.login = res['login']
        user.avatar_url = res['avatar_url']
        user.url = res['html_url']
        user.email = res['email']
        user.blog = res['blog']
        user.save()
    except User.DoesNotExist:
        user = User(id=res['id'], login=res['login'], avatar_url=res['avatar_url'], url=res['html_url'],
                    name=res['name'], email=res['email'], blog=res['blog'])
        user.save()
    request.session['islogin'] = res['id']
    request.session['username'] = res['name']
    request.session['avatar_url'] = res['avatar_url']
    return render(request, 'blogv3/html/welcome.html', context={"user": user})


def comment(request):
    # 处理不是 POST的请求 先省略
    # if request.method != 'POST':
    #     return Http404()

    textarea = request.POST.get('textarea', None)
    code = request.POST.get('code', None)
    art_id = request.POST.get('artid', None)
    if not textarea or not code:
        return JsonResponse({'info': 0})
    code_s = request.session.get('captcha', None)
    if code_s == None:
        # 重新验证
        return JsonResponse({'info': 3})
    if code.lower() != code_s.lower():
        return JsonResponse({'info': 1})

    # 字数限制
    if len(textarea) > 300:
        return JsonResponse({'info': 4})

    # 对提交的内容进行过滤 xss 检测 错误返回 2
    #********先省略, 先写后面的逻辑******

    # 准确无误后入库
    # 获取ip
    ip = request.META['REMOTE_ADDR']
    # 获取user
    user_id = request.session.get('islogin', None)
    user = getuser(user_id)
    if user == None:
        # 重新验证
        del request.session['islogin']
        return JsonResponse({'info': 3})
    # 获取文章
    art = getart(art_id)
    art.article_commentnum += 1
    art.save()
    # 获取类型
    types = art.article_type
    from .models import Comment
    from datetime import datetime
    nowtime = datetime.now()
    com = Comment(com_article=art, com_type=types, com_user=user, com_content=textarea, com_ip=ip, com_date=nowtime)
    com.save()
    from django.core.mail import send_mail
    title = user.name + "评论了您的文章" + art.article_title
    Thread(target=sendmail, args=(title, textarea)).start()
    return JsonResponse({'info': 3, "comtent": textarea, 'user': user.name, 'date': nowtime.strftime("%Y年%m月%d日 %H:%M")})


def labelcloud(request, pk):

    type_id = gettype_id(pk)

    if type_id == None:
        arts = []
    else:
        from .models import Article
        arts = Article.objects.filter(article_type=type_id)
        for art in arts:
            art.article_content = markdown(art.article_content, extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.abbr",
                "markdown.extensions.attr_list",
                "markdown.extensions.def_list",
                "markdown.extensions.fenced_code",
                "markdown.extensions.footnotes",
                "markdown.extensions.tables",
                "markdown.extensions.smart_strong",
                "markdown.extensions.admonition",
                "markdown.extensions.codehilite",
                "markdown.extensions.headerid",
                "markdown.extensions.meta",
                "markdown.extensions.nl2br",
                "markdown.extensions.sane_lists",
                "markdown.extensions.smarty",
                "markdown.extensions.toc",
                "markdown.extensions.wikilinks"])
    # 读取标签
    types = gettypes()
    # 热门文章(浏览量)
    hotarts = Article.objects.order_by('-article_scannum')[:5]
    colors = ["btn-primary", "btn-info", "btn-success", "btn-danger", "btn-warning", "btn-rose"]
    sizes = ["btn-sm", "btn-lg", ""]
    return render(request, 'blogv3/html/labelcloud.html',
                  context={'arts': arts, 'types': types, 'hotarts': hotarts, 'year_month_number': getarching(),
                  "colors": colors, "sizes": sizes, "label": type_id})


def sendmail(title, msg):
    from django.core.mail import send_mail
    send_mail(title, msg, '18238670823@163.com',
              ['ilovejdl@126.com'], fail_silently=False)


def gettypes():
    from .models import Type
    return ["".join(x) for x in Type.objects.values_list('type_content')]


def gettype_id(ty):
    from .models import Type
    try:
        return Type.objects.get(type_content=ty)
    except Type.DoesNotExist:
        return None


def getpages(val, nowpage):
    if val < 10:
        return range(1, val+1)
    else:
        if nowpage - 1 <= 4:
            page_list = list(range(1, nowpage+3))
            page_list.append('...')
            page_list.append(val)
            return page_list
        elif val - nowpage <= 4:
            page_list = list(range(nowpage - 2, val+1))
            return [1] + ['...'] + page_list
        else:
            page_list = list(range(nowpage - 2, nowpage + 3))
            return [1] + ['...'] + page_list + ['...'] +[val]


def code(requset):
    from io import BytesIO
    from tools.GetCode import getcode
    f = BytesIO()
    img, code = getcode().create()
    # 记得 添加session
    requset.session['captcha'] = code
    img.save(f, "PNG")
    return f.getvalue()


def getarching():
    from .models import Article
    articles = Article.objects.values('article_date')
    year_month = set()
    for i in articles:
        year_month.add((i['article_date'].strftime("%Y"), i['article_date'].strftime("%m")))
    conter = {}.fromkeys(year_month, 0)
    for i in articles:
        conter[(i['article_date'].strftime("%Y"), i['article_date'].strftime("%m"))] += 1

    year_month_number = []
    for key in conter:
        # year_month_number.append([key[0], key[1], conter[key]])
        # year_month_number.append(key[0] + "年" + key[1] + "月" + "("+ str(conter[key]) + ")")
        year_month_number.append({"date": key[0] + "年" + key[1] + "月","conter": conter[key]})
    year_month_number.sort(key=lambda x: x["date"], reverse=True)
    return year_month_number


def getuser(id):
    from .models import User
    try:
        return User.objects.get(id= id)
    except User.DoesNotExist:
        return None


def getart(id):
    from .models import Article
    try:
        return Article.objects.get(article_id=id)
    except Article.DoesNotExist:
        return None


def getcoments(art):
    from .models import Comment
    coms = Comment.objects.filter(com_article=art).order_by("-com_date")
    return coms


# 404 页面

def page_not_found(request):
    return render(request, '404.html')


# 自定义 tag
@register.tag
def setting_value(name):
    return getart(settings.name)

