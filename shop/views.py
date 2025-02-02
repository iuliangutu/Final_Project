from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from .forms import ProductForm
from .models import Category, Seller, Product, ProductType, OrderLine, Order, Cart


# Create your views here.

class ProductView(ListView):
    template_name = 'products.html'
    model = Product

    def get_queryset(self):
        # Start with all products
        products = Product.objects.all()

        # Get rating filter from GET request
        rating = self.request.GET.get('rating', '')
        if rating:
            # Filter by rating if specified
            products = products.filter(rating=rating)

        # Get price sorting option from GET request
        price = self.request.GET.get('price', '')
        if price == 'ascending':
            products = products.order_by('price')  # Ascending order
        elif price == 'descending':
            products = products.order_by('-price')  # Descending order

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the rating and price_order to context so they can be used in the template
        context['rating'] = self.request.GET.get('rating', '')
        context['price_order'] = self.request.GET.get('price_order', '')
        return context



class ProductViewDetail(DetailView):
    template_name = 'products_detail.html'
    model = Product


class CategoryProductView(ListView):
    template_name = 'products.html'
    model = Product
    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category_name'])
        products = Product.objects.filter(category=category)
        # Get rating filter from GET request
        rating = self.request.GET.get('rating', '')
        if rating:
            # Filter by rating if specified
            products = products.filter(rating=rating)
        # Get price sorting option from GET request
        price = self.request.GET.get('price', '')
        if price == 'ascending':
            products = products.order_by('price')  # Ascending order
        elif price == 'descending':
            products = products.order_by('-price')  # Descending order
        return products
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name=self.kwargs['category_name'])
        context['category_name'] = category.name
        context['rating'] = self.request.GET.get('rating', '')
        context['price_order'] = self.request.GET.get('price', '')
        return context

class CategoryView(ListView):
    template_name = 'categories.html'
    model = Category


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




