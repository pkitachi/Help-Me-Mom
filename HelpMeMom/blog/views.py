from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments, Coins
from .forms import AddComment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
								 DetailView,
	  							CreateView,
	  							UpdateView,
	  							DeleteView)

from django.contrib import messages
from django.db.models import Q
import requests
# from rake_nltk import Rake
# from guesslang import Guess
import random
# from django.shortcuts import render_to_response
recipeSearchApiID = '20fba441'
recipeSearchApiKey = 'd31fc8d8700c4bb1addc9195e5e162fe'
# Create your views here.
def home(request):
	context = {
		'posts':Post.objects.all()
	}
	return render(request,'blog/home.html',context)

def about(request):
	# return render(request,'blog/home.html')
	pass

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	# paginating
	paginate_by = 4


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	# paginating
	paginate_by = 4

	def get_queryset(self):
		# capturing username from the url by kwargs
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')


# class PostDetailView(DetailView):
# 	model = Post
# 	# context_object_name = 'o'
# 	# template_name = 'blog/home.html'
# 	# context_object_name = 'posts'
# 	# ordering = ['-date_posted']
	# template_name='blog/post_detail.html'

def PostDetails(request, post_pk):
	post = Post.objects.filter(pk = post_pk)[0]

	if request.method == "POST":
		comment_form = AddComment(request.POST)
		if comment_form.is_valid():
			auth = request.user
			body = comment_form.cleaned_data.get('comment_body')
			# print("*********{}".format(auth.username))
			# print("***********************{}".format(body))

			newcomm = Comments(post=post, comment_author=auth, comment_body=body)
			newcomm.save()
	# else:		
	comment_form = AddComment()
	comments = Comments.objects.filter(post = post)

	return render(request, 'blog/post_detail.html',{'post':post,'comment_form':comment_form, 'comments':comments})

class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		coins = Post.objects.filter(author = self.request.user).count()*10
		c = Coins.objects.filter(author = self.request.user)
		c.update(coinNo = coins)
		self.object = form.save()
		return redirect('blog-home')



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields = ['title','content']
	success_url='/'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		# returns the current object
		# we have to check whether the current user is the author of the current post
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Comments
	fields = ['comment_body']
	success_url='/'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		# returns the current object
		# we have to check whether the current user is the author of the current post
		comment = self.get_object()
		if self.request.user == comment.comment_author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comments
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.comment_author:
            return True
        return False


def SearchPost(request):

	query = request.POST['postsearch']
	print("**************{}".format(query))

	url = f'https://api.edamam.com/search?q={query}&app_id={recipeSearchApiID}&app_key={recipeSearchApiKey}'
	response = requests.get(url)
	j = response.json()

	results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

	# if(len(results) == 0 ):
	# 	messages.error(request, f"Sorry we couldn't find anything related to {query} ")
	# else:
	messages.success(request, f"Results for ' {query} ' are ")

	return render(request, 'blog/search_results.html',{'results':results,'response':j['hits']})


def ApiSearch(request):
	# re
	url = f'https://api.edamam.com/search?q=chicken&app_id={recipeSearchApiID}&app_key={recipeSearchApiKey}&q=chicken'
	response = requests.get(url)
	j = response.json()
	# print(response.text)
	return render(request,'blog/api.html',{'response':j['hits']})
