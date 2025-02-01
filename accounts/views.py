from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView

from accounts.cart import AddToCart
from accounts.forms import SignUpForm
from accounts.models import Profile
from shop.models import Order, OrderLine, Cart, Product, Category
from django.core.mail import send_mail



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

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data

        send_mail('Account registration',
                  'Welcome to Shop Hunters',
                  'huntershopman@gmail.com',
                  [cleaned_data['email']], fail_silently=False)

        return result

def profile_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # messages = AdminRequestMessage.objects.filter(user=request.user)

        return render(request, 'profile.html',
                      context={'profile': profile})

    else:
        return redirect('/accounts/login/')


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=self.request.user)
        try:
            cart = Cart.objects.get(client=profile)
        except:
            cart = ""

        return render(request, template_name='cart.html',
                      context={'cart': cart})


def add_to_cart_view(request, product_id):
    if request.user.is_authenticated:
        quantity = int(request.POST.get('quantity', 1))
        profile = Profile.objects.get(user=request.user)

        # ✅ Ensure only one pending order exists
        order = Order.objects.filter(client=profile, status='pending').first()
        if not order:
            order = Order.objects.create(client=profile, status='pending')


        cart = Cart.objects.filter(client=profile).first()
        if not cart:
            cart = Cart.objects.create(client=profile, order=order)

        # ✅ Fix `product_price` issue (should be product.price)
        cart_instance = AddToCart(request.user)
        cart_instance.add_product(product_id, quantity, product_price=Product.objects.get(pk=product_id).price)

        return redirect(reverse_lazy('accounts:cart'))
    else:
        return redirect(reverse_lazy('accounts:login'))


class OrderLineDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'order_line_confirm_delete.html'
    model = OrderLine
    success_url = reverse_lazy('accounts:cart')

    def delete(self, request, *args, **kwargs):
        order_line = self.get_object()
        order = order_line.product_price  # Get the related order
        response = super().delete(request, *args, **kwargs)
        # Recalculate order total cost
        order.total_cost = sum(item.product.price * item.quantity for item in order.orderline_set.all())
        order.save()
        return response


def payment_proceed_view(request):

    if request.user.is_authenticated:
        try:
            # Get the user's profile
            profile = Profile.objects.get(user=request.user)

            cart = Cart.objects.get(client=profile)
            # print(cart)
            cart.delete()
            Order.objects.create(client=profile, status='pending')

            return redirect('accounts:payment_complete')
        except Profile.DoesNotExist:
            return redirect('accounts:profile')

        except Cart.DoesNotExist:
            return redirect('accounts:cart')
    else:

        return redirect('accounts:login')


def payment_complete_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    # Get the user's profile
    profile = Profile.objects.get(user=request.user)
    cleaned_data = {'email': profile.user.email}
    # Send the confirmation email
    send_mail('Payment confirmation', 'Thank you for your purchase. Your payment was successful.',
              'huntershopman@gmail.com',
              [cleaned_data['email']], fail_silently=False)
    return render(request, 'payment_complete.html')


# o pagina pentru toate orders in care le filtram dupa client.
# dupa request.user luam profilul clientului. Asta e prima pagina.

# a doua pagina in care vad detaliile despre acel order. In pagina asta afisam orderlines pe care le filtram dupa order

# view, template + url


def client_orders_view(request):
    if request.user.is_authenticated:
        client_profile = request.user.profile
        # Exclude the most recent order (by `order_date`)
        last_order = Order.objects.filter(client=client_profile).order_by('-order_date').first()
        if last_order:
            orders = Order.objects.filter(client=client_profile).exclude(id=last_order.id).order_by('-order_date')
        else:
            orders = Order.objects.filter(client=client_profile).order_by('-order_date')
        return render(request, 'client_orders.html', {'orders': orders})
    else:
        return redirect('accounts:login')


def previous_orders_view(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(pk=pk)
        order_lines = OrderLine.objects.filter(product_price=order)
        return render(request, template_name='previous_order_details.html', context={'order_lines':order_lines})

    else:
        return redirect('accounts:login')


