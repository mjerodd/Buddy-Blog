from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import Post, Comments
from app.forms import CommentForm, SubscribeForm
# Create your views here.


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = 'Subscribed Successfully'
            subscribe_form = SubscribeForm()

    context = {'posts': posts,
               'top_posts': top_posts,
               'recent_posts': recent_posts,
               'subscribe_form': subscribe_form,
               'subscribe_successful': subscribe_successful,
               'featured_blog': featured_blog,
               }
    return render(request, "app/index.html", context=context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
                else:
                    comment = comment_form.save(commit=False)
                    postid = request.post.get('post_id')
                    post = Post.objects.get(id=postid)
                    comment.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()

    context = {
        'post': post,
        'form': form,
    }
    return render(request, "app/post.html", context)


def tag_page(request, slug):
    context = {}
    return render(request, 'app/tag.html', context)