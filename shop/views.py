from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Client, Category, Provider, Product, ProductType, OrderLine, Order, Cart


# Create your views here.

class ProductView(ListView):
    template_name = 'products.html'
    model = Product


class ProductViewDetail(DetailView):
    template_name = 'products_detail.html'
    model = Product

    def product_detail(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'products_detail.html',
                      {'product': product})


class ProductCreateView(CreateView):
    template_name = 'form.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')
        return super().form_valid(form)



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

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     order = Order.objects.get(name=self.kwargs[''])


class ProductCreateView(CreateView):
    template_name = 'form.html'
    form_class = ProductForm


class ProductUpdateView(UpdateView):
    template_name = 'form.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product-list')


class ProductDeleteView(DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('product-list')
