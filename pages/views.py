from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import CreateView , UpdateView ,DeleteView
from django.urls import reverse , reverse_lazy
from .models import Article,Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .mixins import FieldMixin,FormValidMixin,AuthorAccessMixin
from django.db.models import Count ,Q
from datetime import datetime,timedelta
from django.contrib.contenttypes.models import ContentType
# Create your views here.
@login_required
def home(request):
	last_month = datetime.today() - timedelta(days=30)
	content_type_id = ContentType.objects.get(app_label="pages", model="article")
	articles_list = Article.objects.filter(private=False)
	paginator = Paginator(articles_list, 3)
	page = request.GET.get("page")
	articles = paginator.get_page(page)
	context = {
	'star': Article.objects.filter(private=False).annotate(
		count=Count('hits',filter=Q(articlehit__created__gt=last_month))
		).order_by('-count','-publish')[:5],
	'starcomment':Article.objects.all().annotate(
		count=Count('comments',filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id))
		).order_by('-count','-publish')[:5],
	'articles' :articles,
	'category':Category.objects.filter(status=True)
	}
	return render(request,'pages/base.html',context)




class PostDetail(LoginRequiredMixin,DetailView):
	template_name = 'pages/detail.html'
	context_object_name = 'article'
	def get_object(self):
		pk = self.kwargs.get("pk")
		article = get_object_or_404(Article.objects.filter(private=False),pk=pk)
		ip_address = self.request.user.ip_address
		if ip_address not in article.hits.all():
			article.hits.add(ip_address)
		return article



@login_required
def category(request,slug):
	context = {
	'category':get_object_or_404(Category,slug=slug,status=True),
	'categorys': Category.objects.all(),
	'article':Article.objects.all()
	}
	return render(request,'pages/category.html',context)

class ListArticle(LoginRequiredMixin,ListView):
	template_name = 'pages/list_article.html'
	def get_queryset(self):
		if self.request.user.is_superuser:
			return Article.objects.all()
		else:
			return Article.objects.filter(author=self.request.user)


class CreateArticle(LoginRequiredMixin,FieldMixin,FormValidMixin,CreateView):
	model = Article
	template_name = 'pages/create_article.html'
	success_url = reverse_lazy('home')

class ArticleUpdate(LoginRequiredMixin,AuthorAccessMixin,FieldMixin,FormValidMixin,UpdateView):
	model = Article
	template_name = 'pages/update_article.html'
	success_url = reverse_lazy('home')

class ArticleDeleteView(LoginRequiredMixin,AuthorAccessMixin,DeleteView):
    model = Article
    success_url = reverse_lazy("list")
    template_name = 'pages/delete_article.html'



def search(request):
	if request.method == "GET":
		searched = request.GET['searched']
		article = Article.objects.filter(Q(post__icontains=searched),private=False)
		return render(request,'pages/search.html',{"searched":searched,'article':article})
	else:
		return render(request,'pages/index.html',{})

