from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
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
	# print("**************{}".format(query))

	results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

	if(len(results) == 0):
		messages.error(request, f"Sorry we couldn't find anything related to {query} ")
	else:
		messages.success(request, f"Results for ' {query} ' are ")

	return render(request, 'blog/search_results.html',{'results':results})



# def Analytics(request):

# 	posts = Post.objects.all()
# 	text =''
# 	total = Post.objects.all().count()
# 	anshm={}
# 	com = Comments.objects.all()
# 	answered = 0
# 	for i in com:
# 		if i.post.id not in anshm:
# 			answered+=1
# 			anshm[i.post.id]=1

# 	r = Rake()
# 	for i in posts:
# 		titletext = i.title
# 		r.extract_keywords_from_text(titletext)
# 		r.get_ranked_phrases()
# 		li = r.get_ranked_phrases_with_scores()

# 		for h in li:
# 			if h[0]<=3:
# 				text = text+(h[-1])
# 				text = text+(h[-1])
# 			else:
# 				for k in range(int(h[0])):
# 					text+=(h[-1])

# 	guess = Guess()
# 	lang = {}
# 	for i in posts:
# 		code = i.content
# 		language = guess.language_name(code)
# 		if language in lang:
# 			lang[language]+=1
# 		else:
# 			lang[language]=1



# 	# print(text)
# 	# print(lang)

# 	# number_of_colors = 8

# 	# color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
# 	# 			for i in range(number_of_colors)]
# 	# print(color)
# 	sort_langs = sorted(lang.items(), key=lambda x: x[1], reverse=True)
# 	print(sort_langs)

# 	langlabels = list()
# 	langvals = list()

# 	for i in sort_langs:
# 		langlabels.append(str(i[0]))
# 		langvals.append(int(i[1]))

# 	langlabels = langlabels[0:5]
# 	# langvals = langvals[0:5]
# 	l1 = langlabels[0]
# 	l2 = langlabels[1]
# 	l3 = langlabels[2]
# 	l4 = langlabels[3]
# 	l5 = langlabels[4]

# 	v1 = langvals[0]
# 	v2 = langvals[1]
# 	v3 = langvals[2]
# 	v4 = langvals[3]
# 	v5 = langvals[4]

# 	print(langlabels)
# 	print(langvals)

# 	return render(request, 'blog/analytics.html',{'text':text, 'langvals':langvals, 'l1':l1,'l2':l2,'l3':l3,'l4':l4,'l5':l5,'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5,'total':total,'answered':answered})


# def some_view(request):
# #    return render_to_response('../../../VidyoConnector/js/VidyoConnector.html')
# 	# return render(request, 'blog/test/VidyoConnector.html')



def ApiSearch(request):
	# re
	url = f'https://api.edamam.com/search?q=chicken&app_id={recipeSearchApiID}&app_key={recipeSearchApiKey}&q=chicken'
	response = requests.get(url)
	j = response.json()
	print(response.text)
	return render(request,'blog/api.html',j)
