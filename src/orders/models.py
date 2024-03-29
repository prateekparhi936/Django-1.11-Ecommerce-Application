from django.db import models
import math
from django.db.models.signals import pre_save,post_save
from Ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile
from addresses.models import Address
# Create your models here.
from carts.models import Cart


ORDER_STATUS_CHOICES = (
		("created","Created"),
		("paid","Paid"),
		("shipped","Shipped"),
		("delievered","Deilevered"),
		("returned","Returned"),
		("refunded","Refunded")
	)

class OrderManager(models.Manager):
	def new_or_get(self,billing_profile,cart_obj):
		order_qs=self.get_queryset().filter(billing_profile=billing_profile,cart=cart_obj,active=True,status="created")
		if order_qs.count()==1:
			created=False
			order_obj=order_qs.first()
		else:
			order_obj=self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
			created=True
		return order_obj,created


class Order(models.Model):
	billing_profile		= models.ForeignKey(BillingProfile,null=True,blank=True)
	shipping_address 	= models.ForeignKey(Address,related_name='shipping_address',null=True,blank=True)
	billing_address		= models.ForeignKey(Address,related_name='billing_address',null=True,blank=True)
	order_id 			= models.CharField(max_length=120,blank=True)
	cart 	 			= models.ForeignKey(Cart)
	status				= models.CharField(max_length=120, default="created" , choices=ORDER_STATUS_CHOICES)
	shipping_total	 	= models.DecimalField(default=5.00,max_digits=100,decimal_places=2)
	total	 			= models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
	active				= models.BooleanField(default=True)

	objects=OrderManager()
	def __str__(self):
		return str(self.order_id)

	def update_total(self):
		cart_total=self.cart.total
		shipping_total=self.shipping_total
		new_total=math.fsum([cart_total,shipping_total])
		self.total=new_total
		self.save()
		return new_total

	def check_done(self):
		billing_profile=self.billing_profile
		billing_address=self.billing_address
		shipping_address=self.shipping_address
		total=self.total

		if billing_profile and billing_address and shipping_address and total>0:
			return True
		return False

	def mark_paid(self):
		if self.check_done():
			self.status="paid"
			self.save()
		return self.status

def pre_save_cart_receiver(sender,instance,*args,**kwargs):
	if not instance.order_id:
		instance.order_id=unique_order_id_generator(instance)
	qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)	

pre_save.connect(pre_save_cart_receiver,sender=Order)

def post_save_cart_total(sender,instance,created,*args,**kwargs):
	if not created:
		cart_obj=instance
		cart_total=cart_obj.total
		cart_id=cart_obj.id
		qs=Order.objects.filter(cart__id=cart_id)
		if qs.count()==1:
			order_obj=qs.first()
			order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
	if created:
		instance.update_total()

post_save.connect(post_save_order,sender=Order)


