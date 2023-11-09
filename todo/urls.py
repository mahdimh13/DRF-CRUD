from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TodoViewSet)

urlpatterns = [
    path('', views.todo_func),
    path('<int:pk>', views.todo_detail_func),
    path('cbv', views.TodoClass.as_view()),
    path('cbv/<int:pk>', views.TodoDetailClass.as_view()),
    path('mixin', views.TodoMixin.as_view()),
    path('mixin/<int:pk>', views.TodoMixinDetail.as_view()),
    path('generic', views.TodoGeneric.as_view()),
    path('generic/<int:pk>', views.TodoGenericDetail.as_view()),
    path('viewsets/', include(router.urls)),
    path('usergeneric', views.UserGeneric.as_view()),
]