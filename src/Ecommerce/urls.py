"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from accounts.views import login_page, register_page, guest_login_page
from addresses.views import checkout_address_create_view
from .views import home_page, about_page, contact_page, logout_page
from carts.views import cart_detail_api_view

urlpatterns = [
	url(r'^$',home_page,name="home"),
	url(r'^about/$',about_page,name="about"),
	url(r'^contacts/$',contact_page,name="contacts"),
	url(r'^login/$',login_page,name="login"),
	url(r'^checkout/address/$',checkout_address_create_view,name="checkout_address"),
	url(r'^api/cart/$',cart_detail_api_view,name="api-cart"),
	# url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name="checkout_address_reuse"),
	url(r'^register/guest/$',guest_login_page,name="guestlogin"),
	url(r'^cart/',include('carts.urls',namespace="cart")),
	url(r'^logout/$',LogoutView.as_view(),name="logout"),
	url(r'^register/$',register_page,name="register"),
	url(r'^products/',include('products.urls',namespace="products")),
	url(r'^search/',include('search.urls',namespace="search")),
	# url(r'^productlist-cbv/$',ProductListView.as_view()),
	# url(r'^productlist-fbv/$',product_list_view),
	# #url(r'^productdetail-cbv/(?P<pk>\d+)/$',ProductDetailView.as_view()),
	# #url(r'^productdetail-fbv/(?P<pk>\d+)/$',product_detail_view),
	# url(r'^productfeatured/$',ProductFeaturedListView.as_view()),
	# url(r'^productfeatured/(?P<pk>\d+)/$',ProductFeaturedDetailView.as_view()),
	# url(r'^products/(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view()),
    url(r'^admin/',admin.site.urls)
]  


if settings.DEBUG:
	urlpatterns = urlpatterns+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)