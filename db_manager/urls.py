from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='orderInfo'),
    path('create', views.create, name='create'),
    path('db_manager/<int:pk>/', views.OrderDetailView.as_view(), name='detail_o'),
    path('db_manager/<int:pk>/update', views.OrderUpdateView.as_view(), name='update_o'),
    path('db_manager/<int:pk>/update_a', views.AOrderUpdateView.as_view(), name='update_ao'),
    path('db_manager/<int:pk>/updatew', views.WOrderUpdateView.as_view(), name='update_wo'),
    path('db_manager/delete', views.delete_order, name='delete_o'),
    path('db_manager/<int:pk>/restart', views.restart_order, name='restart_o'),

    path('confirm/', views.confirm_price, name='confirm'),
    path('confandsend/', views.confandsend, name='confandsend'),
    path('payok/', views.payok, name='payok'),
    path('users/<str:pk>/bonuses/', views.UpdateBonucesView.as_view(), name='bonuses'),
    path('bonuses/set', views.bonuses_set, name='bonuses_set'),

    path('db_manager/detail/<int:pk>/', views.AOrderDetailView.as_view(), name='detail_ao'),
    path('db_manager/detailw/<int:pk>/', views.WOrderDetailView.as_view(), name='detail_wo'),
    path('db_manager/detaildone/<int:pk>/', views.DorderDetailView.as_view(), name='detail_do'),
    path('db_manager/detailco/<int:pk>/', views.CorderDetailView.as_view(), name='detail_co'),
    path('db_manager/<int:pk>/confirmmyprice/<int:pk_2>', views.PAYS_UPDATE.as_view(), name='confirmmyprice'),

    path('wo', views.wo, name='wo'),
    path('price', views.priceO, name='priceO'),
    path('active', views.activeO, name='activeO'),
    path('canceled', views.canceledO, name='canceledO'),
    path('waitOh', views.waitOh, name='waitOh'),
    path('dpo', views.DpO, name='dpo'),
    path('done', views.DoneO, name='doneO'),
    path('authors', views.authors, name='authors'),
    path('users', views.users, name='users'),


]
