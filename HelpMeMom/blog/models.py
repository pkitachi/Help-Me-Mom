from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField(blank=False)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# kwargs is like an argument
		return reverse('post-detail', kwargs={'pk':self.pk})


class Comments(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment_author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	comment_body = models.TextField()
	comment_date = models.DateField(default=timezone.now)

	def __str__(self):
		return f'{self.post.title} by {self.comment_author.username} -> Comment'
