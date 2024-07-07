from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create_character/', views.create_character, name='create_character'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sell_item/<int:item_id>/', views.sell_item, name='sell_item'),
    path('shop/', views.shop, name='shop'),
    path('buy_item/<int:item_id>/', views.buy_item, name='buy_item'),
    path('battle/', views.battle, name='battle'),
    path('battle/action/', views.battle_action, name='battle_action'),
    path('battle/result/', views.battle_result, name='battle_result'), 
    path('', views.index, name='index'),
]
