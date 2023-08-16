from django.db import models
from accounts.models import User
from django.utils import timezone
from extensions.utils import jalali_converter

from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment

class Category(models.Model):
	title = models.CharField(max_length=200,verbose_name="عنوان دسته بندی")
	slug = models.SlugField(max_length=100,unique=True,verbose_name="ادرس دسته بندی")
	status = models.BooleanField(default=True,verbose_name="آیا می خواید نمییش داداه شود؟")
	position = models.IntegerField(verbose_name="پوزیشن")
	class Meta:
		verbose_name="دسته بندی"
		verbose_name_plural = "دسته بندی ها"
		ordering = ['position']
	def __str__(self):
		return self.title


class IPAddress(models.Model):
	ip_address = models.GenericIPAddressField(verbose_name="آدرس ای پی")


class Article(models.Model):
	post = models.TextField(max_length = 1000,unique=False,verbose_name='Post')
	pictures = models.ImageField(upload_to="images/",unique=False,verbose_name='Image',null=True,blank=True)
	category = models.ManyToManyField(Category,verbose_name='category',related_name='articles',null=True,blank=True,)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	private = models.BooleanField(default=False,verbose_name="Private")
	video = models.FileField(upload_to='video/',verbose_name="Video",null=True,blank=True)
	comments = GenericRelation(Comment)
	hits = models.ManyToManyField(IPAddress,through="ArticleHit",blank=True,related_name="hits",verbose_name="Views")
	





	def __str__(self):
		return self.post
	class Meta:
		verbose_name="پست"
		verbose_name_plural = "پست ها"
		ordering =['-publish']
	def category_published(self):
		return self.category.filter(status=True)
	
	def jpublish(self):
		return jalali_converter(self.publish)
	jpublish.short_description = "زمان انتشار پست"

	def category_to_str(self):
		return " ".join([category.title for category in self.category.all()])
	category_to_str.short_description = 'دسته بندی'
	


class ArticleHit(models.Model):
	article = models.ForeignKey(Article,on_delete=models.CASCADE)
	ip_address = models.ForeignKey(IPAddress,on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
