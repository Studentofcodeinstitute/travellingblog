from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import Post
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )

class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

class PostCreateView(View):

    def get(self, request, *args, **kwargs):
        form = PostForm()
    

        return render(
            request,
            "post_create.html",
            {
                "form": form
            },
        )
    #def get(self, request, slug, *args, **kwargs):
        #queryset = Post.objects.filter(status=1)
        #post = get_object_or_404(queryset, slug=slug)
        #forms = post.forms.filter(approved=True).order_by("-created_on")
        #liked = False
        #if post.likes.filter(id=self.request.user.id).exists():
            #liked = True

        #return render(
            #request,
            #"post_create.html",
            #{
                #"form": form,
                #"created": False,
                #"liked": liked,
                #"form": PostForm()
            #},
        #)

    #def post(self, request, slug, *args, **kwargs):

        #queryset = Post.objects.filter(status=1)
        #post = get_object_or_404(queryset, slug=slug)
        #formss = post.forms.filter(approved=True).order_by("-created_on")
        #liked = False
        #if post.likes.filter(id=self.request.user.id).exists():
            #liked = True

        #form = PostForm(data=request.POST)
        #if form.is_valid():
            #form.instance.email = request.user.email
            #form.instance.name = request.user.username
            #form = form.save(commit=False)
            #form.post = post
            #form.save()
        #else:
            #form = PostForm()

        #return render(
            #request,
            #"post_create.html",
            #{
            
                #"form": form,
                #"created": True,
                #"liked": liked,
                #"form": PostForm()
            #},
        #)
    #def post(self, request, slug, *args, **kwargs):

        

class PostUpdateView(View):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(View):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False