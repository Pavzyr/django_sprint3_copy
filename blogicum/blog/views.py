from blog.models import Category, Post
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils import timezone


def get_post_list():
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    return post_list


def index(request):
    template = 'blog/index.html'
    context = {'post_list': get_post_list()[:settings.NUM_OF_PUNBLIC]}
    # NUM_OF_PUNBLIC вынесен в константы в settings.py
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    context = {'post': get_object_or_404(get_post_list(), pk=id)}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    context = {
        'category': category,
        'post_list': get_post_list().filter(category=category)
    }
    return render(request, template, context)