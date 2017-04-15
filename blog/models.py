from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

# Create your models here.


class BlogAuthor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.CharField(max_length=200,help_text='Enter Your Biography')

    def __str__(self):
        return 'Blog author name is %s' % self.name

    def get_absolute_url(self):
        return reverse('blogs-by-author', args=str(self.id))


class Blog(models.Model):

    name = models.CharField(max_length=200,help_text='Enter The name of Blog.')
    description = models.TextField(max_length=2000, help_text='Enter your blog text here.')
    author =  models.ForeignKey(BlogAuthor,on_delete=models.SET_NULL,null=True)
    post_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog-detail',args=str(self.id))


class BlogComment(models.Model):
    description = models.TextField(max_length=1000,help_text='Enter your Coment Here')
    post_date = models.DateTimeField(auto_now_add=date)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        len_title = 75
        if len(self.description)>len_title:
            title_string = self.description[:len_title]
        else:
            title_string = self.description
        return title_string
