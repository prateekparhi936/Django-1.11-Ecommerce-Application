from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from products.models import Product
from django.db.models import Q
from carts.models import Cart

#Create your views here
class ProductFeaturedListView(ListView):
	template_name="product/list-feature.html"
	def get_queryset(self,*args,**kwargs):
		request=self.request
		print(Product.objects.featured())
		return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
	queryset=Product.objects.featured()
	template_name="product/detail-feature.html"
	# def get_queryset(self,*args,**kwargs):
	# 	request=self.request
	# 	return Product.objects.featured()





##class Based ListView
class ProductListView(ListView):
	#query_set=Product.objects.featured()
	template_name="product/list.html"

	def get_context_data(self, **kwargs):
	    context = super(ProductListView, self).get_context_data(**kwargs)
	    request=self.request
	    cart_obj,new_obj=Cart.objects.new_or_get(request)
	    context['cart']=cart_obj
	    return context

	def get_queryset(self,*args,**kwargs):
		request=self.request
		return Product.objects.all()


##Function Based ListView
def product_list_view(request):
	query_set=Product.objects.all()		#select * from table  ||        objects is the source that retrieved data
	context={
		"qs":query_set
	}
	return render(request,"product/list.html",context)





##Class Based DetailView
class ProductDetailView(DetailView):
	#query_set=Product.objects.all()
	template_name="product/detail.html"
	
	def get_context_data(self, **kwargs):
	    context = super(ProductDetailView,self).get_context_data(**kwargs)
	    return context

	def get_object(self,*args,**kwargs):
		request=self.request
		pk=self.kwargs.get('pk')
		instance=Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product Does Not Exists!!")
		return instance
	
	# def get_queryset(self,*args,**kwargs):
	# 	request=self.request
	# 	pk=self.kwargs.get('pk')
	# 	return Product.objects.filter(pk=pk)




##Function Based DetailView
def product_detail_view(request,pk=None,*args,**kwargs):
	# instance=get_object_or_404(Product,pk=pk)
	instance=Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product Does Not Exists!!")

	context={
		"qs":instance
	}
	return render(request,"product/detail.html",context)



##Slug View
class ProductDetailSlugView(DetailView):
	query_set=Product.objects.all()
	template_name="product/detail.html"

	def get_context_data(self, **kwargs):
	    context = super(ProductDetailSlugView, self).get_context_data(**kwargs)
	    request=self.request
	    cart_obj,new_obj=Cart.objects.new_or_get(request)
	    context['cart']=cart_obj
	    return context

	def get_object(self,*args,**kwargs):
		request=self.request
		slug=self.kwargs.get('slug')
		instance=get_object_or_404(Product,slug=slug,active=True)
		return instance
