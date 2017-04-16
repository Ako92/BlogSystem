from django.shortcuts import render
from .models import Blog, BlogAuthor, BlogComment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    """
     View function for home page of site.
     """
    # Render the HTML template index.html
    return render(
        request,
        'index.html',
    )


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5


class BlogListByAuthorView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListByAuthorView, self).get_context_data(**kwargs)
        # Get the blogger information
        id = self.kwargs['pk']
        target_blogger = get_object_or_404(BlogAuthor, pk=id)
        # Add in a QuerySet of all the books
        context['blogger'] = target_blogger
        return context


class BlogDetailView(generic.DetailView):
    model = Blog


class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 5


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = BlogComment
    fields = ['description']

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # get the blog from id ad add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        add author and associated blog to form data before setting it as valid (so it's saved to models)

        """
        # add logged in user as author of comment
        form.instance.author = self.request.user
        # associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        after posting comment return associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })
