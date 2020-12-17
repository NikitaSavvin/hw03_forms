from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


def index(request):
    latest = Post.objects.all()
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    return render(request, 'group.html', {'group': group, 'posts': posts})


@login_required
def post_new(request):
    form = PostForm(request.POST)
    if not request.method == 'POST':
        return render(request, 'post_new.html', {'form': form})
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('index')
    form = PostForm()
    return render(request, 'post_new.html', {'form': form})
