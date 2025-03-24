from django.urls import path
from goose_farmer_game import views
from knox import views as knox_views

from .views import BirdTypeViewSet, BirdViewSet, DropWeightsViewSet, SummonBirdView

bird_type_list = BirdTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bird_type_detail = BirdTypeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

bird_list = BirdViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bird_detail = BirdViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

drop_weight_list = DropWeightsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
drop_weight_detail = DropWeightsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('test/', views.TestView.as_view()),
    path('verify/', views.VerificationView.as_view()),
    path('bird-types/', bird_type_list),
    path('bird-types/<int:pk>', bird_type_detail),
    path('birds/', bird_list),
    path('birds/<int:pk>', bird_detail),
    path('drop-weights/', drop_weight_list),
    path('drop-weights/<int:pk>', drop_weight_detail),
    path('summon', SummonBirdView.as_view()),
]
