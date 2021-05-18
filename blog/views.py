from django.shortcuts import render, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.views.generic import ListView
from django.core.mail import send_mail

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3)
#     page = request.GET.get('page')

#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request,'blog/post/list.html', {'posts': posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, 
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status='published'
    )

    comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(data=request.POST)

        if form.is_valid():
            cd = form.clean()
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post , 'comments':comments, 'form': form})


def post_share(request, post_id):
    post = get_object_or_404(Post,id= post_id)
    sent = False

    if request.method == "GET":
        form = EmailPostForm()
    else:
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cd = form.clean()

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends that you read {post.title}"
            message = f"Read {post.title} at {post_url} \n {cd['name']}\'s comments: {cd['comments']}"
            
            send_mail(subject, message, 'admin@blog.com', [cd['to']] )
            sent = True
    return render(request, 'blog/post/share.html', {'form': form, 'sent': sent, 'post': post})

