from django.urls import path
from . import views

urlpatterns = [
    path('auction_dashboard/', views.auction_dashboard, name='auction_dashboard'),
    path('auction_cart/', views.cart_detail, name='auction_cart'),
    path('auction_checkout/', views.payment, name='auction_checkout'),
    path('auction/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('auction/<int:auction_id>/bid/', views.auction_bid, name='auction_bid'),
    path('auction/<int:auction_id>/close/', views.auction_close, name='auction_close'),
    path('auction/<int:auction_id>/comment/', views.auction_comment, name='auction_comment'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/bid/', views.place_bid, name='place_bid'),
    path('item/<int:item_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'), 
    path('payment/', views.payment, name='payment'),
    path('process_payment/<str:client_secret>/', views.process_payment, name='process_payment'),   
    # Add other URLs as needed
]
