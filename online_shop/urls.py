"""
URL configuration for online_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shop.views import ProductView, OrderView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ProductViewDetail
from accounts import urls as accounts_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urls, namespace='accounts')),
    path('', ProductView.as_view(), name='product-list'),
    path('create', ProductCreateView.as_view(success_url='/'), name='product-create'),
    path('update', ProductUpdateView.as_view(), name='product-update'),
    path('delete', ProductDeleteView.as_view(), name='product-delete'),
    path('product/<pk>', ProductViewDetail.as_view(), name='product-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
