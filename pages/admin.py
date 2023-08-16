from django.contrib import admin
from .models import Article,Category,IPAddress
# Register your models here.


	
class ArticleAdmin(admin.ModelAdmin):
	list_display = ['post','pictures','category_to_str','jpublish','private','video'] 
	search_fields = ('post','author')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['position','title','slug','status',] 
	list_filter = (['status'])
	search_fields = ('post','slug')



admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(IPAddress)