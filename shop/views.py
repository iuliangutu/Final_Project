from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Category, Seller, Product, ProductType, OrderLine, Order, Cart


# Create your views here.

class ProductView(ListView):
    template_name = 'products.html'
    model = Product


class ProductViewDetail(DetailView):
    template_name = 'products_detail.html'
    model = Product


class CategoryProductView(ListView):
    template_name = 'products.html'
    model = Product
    def get_queryset(self):
        qs = super().get_queryset()
        category = Category.objects.get(name=self.kwargs['category_name'])
        return qs.filter(category=category)

class CategoryView(ListView):
    template_name = 'categories.html'
    model = Category

# def category_filter(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     products = Product.objects.filter(category=category)
#     return render(request, 'products.html', {'products': products, 'category': category})






class ProductCreateView(CreateView):
    template_name = 'form.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("User provided invalid data")
        # print(form.errors)
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    template_name = 'form.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product-list')


class ProductDeleteView(DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('product-list')


class OrderView(ListView):
    template_name = 'products.html'
    model = Product

