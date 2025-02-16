from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from .forms import ProductForm
from .models import Category, Product

class ProductView(ListView):
    template_name = 'products.html'
    model = Product
    def get_queryset(self):
        products = Product.objects.all()
        # Get filters from GET request
        rating = self.request.GET.get('rating', '')
        price = self.request.GET.get('price', '')
        search_query = self.request.GET.get('search', '')
        # Apply rating filter
        if rating:
            products = products.filter(rating=rating)
        # Apply price sorting
        if price == 'ascending':
            products = products.order_by('price')
        elif price == 'descending':
            products = products.order_by('-price')
        # Apply search filter
        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return products
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the rating, price, and search to context so they can be used in the template
        context['rating'] = self.request.GET.get('rating', '')
        context['price'] = self.request.GET.get('price', '')
        context['search'] = self.request.GET.get('search', '')
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
        # Get filters from GET request
        rating = self.request.GET.get('rating', '')
        price = self.request.GET.get('price', '')
        search_query = self.request.GET.get('search', '')
        # Apply rating filter
        if rating:
            products = products.filter(rating=rating)
        # Apply price sorting
        if price == 'ascending':
            products = products.order_by('price')
        elif price == 'descending':
            products = products.order_by('-price')
        # Apply search filter
        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name=self.kwargs['category_name'])
        context['category_name'] = category.name
        context['rating'] = self.request.GET.get('rating', '')
        context['price'] = self.request.GET.get('price', '')
        context['search'] = self.request.GET.get('search', '')
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

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')