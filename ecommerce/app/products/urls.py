from django.urls import path , include

from . import views

urlpatterns = [
    path('',views.home, name="home_page"),
    path('electronics/', views.electronics, name="electronic_page"),

    # admin controll

    path('admin/dashboard/',views.admin_dashboard,name='admin_dashbaord'),
    path('admin/product/add',views.add_product, name='add_product'),


    path('admin/category/add',views.add_category, name='add_category'),
    path('admin/category/list',views.category_list, name='category_list'),
    path('admin/role/add',views.add_user_role, name='add_role'),


    # authentication
    path('account/register/',views.user_registration, name='register_user'),
   
  
]

