from django.shortcuts import render
from django.db.models import Q
from django.views.generic.list import ListView

from products.models import Product

##class Based ListView
class SearchProductView(ListView):
	template_name="search/view.html"

	def get_context_data(self, **kwargs):
	    context = super(SearchProductView, self).get_context_data(**kwargs)
	    context['query']=self.request.GET.get('q');			## can use {{query}} in html pages to get the searched string
	    return context

	def get_queryset(self,*args,**kwargs):
		request=self.request
		search_query=request.GET.get('q',"Tshirt")
		print(search_query)
		if search_query is not None:
			return Product.objects.search(search_query)
		else:
			Product.objects.featured()