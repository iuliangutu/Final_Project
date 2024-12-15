from django.contrib.auth.views import LogoutView
from django.urls import path
from accounts.views import profile_view, CartView, add_to_cart_view, OrderLineDeleteView

from accounts.views import SubmittableLoginView, SubmittablePasswordChangeView, SignUpView
from shop.views import ProductView

app_name = 'accounts'
urlpatterns = [
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password', SubmittablePasswordChangeView.as_view(), name='password-change'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('profile/', profile_view, name='profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<product_id>/', add_to_cart_view, name='add-to-cart'),
    path('delete/<pk>', OrderLineDeleteView.as_view(), name='delete')
]