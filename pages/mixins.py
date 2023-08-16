from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Article
class FieldMixin():
    def dispatch(self, request, *args ,**kwargs):
        if request.user.is_superuser:
            self.fields = ('post','pictures','author','category','video','publish','private')
        else:
            self.fields = ('post','pictures','category','video','private')
        return super().dispatch(request,*args,**kwargs)
class FormValidMixin():
    def form_valid(self,form):
        if self.request.user.is_superuser:
            form.save()
        else:
            obj = form.save(commit=False)
            obj.author = self.request.user
        return super().form_valid(form)
class AuthorAccessMixin():
    def dispatch(self, request,pk, *args ,**kwargs):
        article = get_object_or_404(Article,pk=pk)
        if article.author == request.user or request.user.is_superuser:
            return super().dispatch(request,*args,**kwargs)
        else:
            raise Http404("You can't see this pages.")