from django.shortcuts import render
from datetime import date
from .models import Post,Author,Tag
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView
from .forms import CommentForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
def get_date(post):
    return post['date']

# Create your views here.
# def starting_page(request):
#     posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html",{
#         "posts":posts
#     })

class StartingPageView(ListView):
    template_name="blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name="posts"
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# automatically looks at blog's templates


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request,"blog/all-posts.html",{
#         "all_posts":all_posts#adds all post variable into allposts.html template
#     })
class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name ="all_posts"
    
    
# class PostDetailView(DetailView):
#     template_name ="blog/post-detail.html"
#     model = Post
#     context_object_name="post"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tag.all()
#         context["comment_form"] = CommentForm()
#         return context

class PostDetailView(View):
    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post.id in stored_posts
        else:
            is_saved_for_later = False
        context = {
            "post":post,
            "post_tags":post.tag.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":is_saved_for_later
        }
        return render(request,"blog/post-detail.html",context)
    
    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))

        context = {
            "post":post,
            "post_tags":post.tag.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)
        
    
# def post_detail(request,slug):
#     # post = next(post for post in all_posts if post['slug']==slug)
#     post = get_object_or_404(Post,slug=slug)
#     return render(request,"blog/post-detail.html",{
#         'post':post,
#         'post_tags':post.tag.all()
#     })
class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context={}
        if stored_posts is None or len(stored_posts) ==0:
            context["posts"] =[]
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/stored_posts.html",context)
            
    def post(self,request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = [] 
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
        return HttpResponseRedirect("/")
        