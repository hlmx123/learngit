from math import ceil

from django.shortcuts import render, redirect

from post.helper import page_cache, read_count, get_top_n, is_login
from post.models import Post



@page_cache(60)
def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码
    total = Post.objects.count()            # 帖子总数
    per_page = 10                           # 每页帖子数
    pages = ceil(total / per_page)          # 总页数

    start = (page - 1) * per_page
    end = start + per_page

    posts = Post.objects.all().order_by('-id')[start:end]  # 惰性加载 懒加载
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(pages)})

@is_login
def create_post(request):
    # user_login=request.session.get('nickname')
    # if user_login:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            post = Post.objects.create(title=title, content=content)
            return redirect('/post/read/?post_id=%s' % post.id)
        return render(request, 'create_post.html')
    # return redirect('/user/login/')
@is_login
def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.tag = request.POST.get('tag')
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post': post})

@read_count
@page_cache(5)
def read_post(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(id=post_id)

    return render(request, 'read_post.html', {'post': post})


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})

def top10(request):
    '''
    rank_data = [
        [<Post(37)>, 128],
        [<Post(32)>,  96],
        [<Post(25)>,  89],
        [<Post(11)>,  71],
    ]
    '''
    rank_data = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': rank_data})
