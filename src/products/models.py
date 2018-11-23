
from django.db import models
import random
import os
from django.db.models import Q

# Create your models here.

def get_file_ext(filepath):
	base_name=os.path.basename(filepath)
	ext=os.path.splitext(base_name)
	return base_name,ext

def upload_path(instance,filename):
	new_name=random.randint(1,9999)
	name,ext=get_file_ext(filename)
	final_name='{new_name}{ext}'.format(new_name=new_name,ext=ext)
	return "products/{new_name}/{final_name}".format(new_name=new_name,final_name=final_name)




##Customer QuerySet
class ProductQuerySet(models.query.QuerySet):			

	def active(self):
		return self.filter(active=True)

	def featured(self):									## this is the custom queryset function
		return self.filter(featured=True)

	def search(self,query):
		lookups=Q(title__icontains=query) | Q(desc__icontains=query) | Q(tag__title__icontains=query)
		return self.filter(lookups).distinct()


##Custom Model-Manager
class ProductManager(models.Manager):

	def get_queryset(self):
		return ProductQuerySet(self.model,using=self._db)

	def featured(self):
		return self.get_queryset().featured()			##calls the custom query set  which is featured()

	def all(self):
		return self.get_queryset().active()

	def get_by_id(self,id):
		qs=self.get_queryset().filter(id=id)
		if qs.count()==1:
			return qs.first()
		else:
			return None

	def search(self,query):
		return self.get_queryset().active().featured().search(query)



class Product(models.Model):
	title=models.CharField(max_length=100)
	slug=models.SlugField(blank=True,unique=True)
	desc=models.TextField()
	price=models.DecimalField(null=False,decimal_places=2,max_digits=20,default=39.99)
	image=models.ImageField(upload_to=upload_path,null=True,blank=True)
	featured=models.BooleanField(default=False)
	active=models.BooleanField(default=True)
	timestamp=models.DateTimeField(auto_now_add=True)

	objects=ProductManager()

	def get_url(self):
		return "/products/{slug}/".format(slug=self.slug)

	def __str__(self):
		return self.title	