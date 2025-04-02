from django.urls import path
from goose_farmer_game import views
from knox import views as knox_views


bird_type_list = views.BirdTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bird_type_detail = views.BirdTypeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

bird_list = views.BirdViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bird_detail = views.BirdViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

drop_weight_list = views.DropWeightsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
drop_weight_detail = views.DropWeightsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('validate-token/', views.ValidateTokenView.as_view()),
    path('verify/', views.VerificationView.as_view()),
    path('bird-types/', bird_type_list),
    path('bird-types/<int:pk>', bird_type_detail),
    path('birds/', bird_list),
    path('birds/<int:pk>', bird_detail),
    path('drop-weights/', drop_weight_list),
    path('drop-weights/<int:pk>', drop_weight_detail),
    path('summon', views.SummonBirdView.as_view()),
]

urlpatterns += [
    path('player/birds/', views.PlayerBirdsView.as_view()),
    path('player/activate-bird', views.ActivateBirdView.as_view())
]