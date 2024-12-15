from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView

from accounts.cart import AddToCart
from accounts.forms import SignUpForm
from accounts.models import Profile
from shop.models import Order, OrderLine, Cart, Product


# Create your views here.

class SubmittableLoginView(LoginView):
    template_name = 'login.html'

class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = '/'

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'

def profile_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # messages = AdminRequestMessage.objects.filter(user=request.user)

        return render(request, 'profile.html',
                      context={'profile': profile})

    else:
        return redirect('/accounts/login/')


# class CartView(LoginRequiredMixin):
#     template_name = 'cart.html'
#     model = Cart
#     login_url = '/accounts/login/'
#     redirect_field_name = 'redirect_to'
#
#
#
#     def get_queryset(self):
#         profile = Profile.objects.get(user=self.request.user)
#         return Cart.objects.filter(client=profile)


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=self.request.user)
        cart = Cart.objects.get(client=profile)
        return render(request, template_name='cart.html',
                      context={'cart': cart})


    # def actor_detail(request, actor_id):
    #     actor = get_object_or_404(Actor, id=actor_id)
    #     return render(request, 'actor_details.html', {'actor': actor})


def add_to_cart_view(request, product_id):
    if request.user.is_authenticated:
        quantity = int(request.POST.get('quantity', 1))
        cart = AddToCart(request.user)
        cart.add_product(product_id, quantity, product_price=cart.order)
        return redirect(reverse_lazy('accounts:cart'))
    else:
        return redirect(reverse_lazy('accounts:login'))

# de adaugat functionalitatea ca userul sa se logheze
# atunci cand vrea sa faca o comanda

class OrderLineDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'order_line_confirm_delete.html'
    model = OrderLine
    success_url = reverse_lazy('accounts:cart')


