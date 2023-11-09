from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Todo
from .serializer import TodoSerializer, UserSerializer

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets

# region function base view
@api_view(['GET', 'POST'])
def todo_func(request: Request):
    if request.method == 'GET':
        todo = Todo.objects.order_by('priority').all()
        serialized_todo = TodoSerializer(todo, many=True)
        print(todo)
        return Response(serialized_todo.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        serialized_todo = TodoSerializer(data=request.data)
        if serialized_todo.is_valid():
            serialized_todo.save()
            return Response(serialized_todo.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def todo_detail_func(request:Request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        todo_serialized = TodoSerializer(todo)
        return Response(todo_serialized.data, status.HTTP_200_OK)
    if request.method == 'PUT':
        todo_serialized = TodoSerializer(todo, data=request.data)
        if todo_serialized.is_valid():
            todo_serialized.save()
            return Response(todo_serialized.data,status.HTTP_200_OK)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_200_OK)

# endregion

# region class base view


class TodoClass(APIView):
    def get(self, request: Request):
        todo = Todo.objects.order_by('priority').all()
        serialized_todo = TodoSerializer(todo, many=True)
        return Response(serialized_todo.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serialized_todo = TodoSerializer(data=request.data)
        if serialized_todo.is_valid():
            serialized_todo.save()
            return Response(serialized_todo.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)


class TodoDetailClass(APIView):
    def get_object(self, pk:int):
        try:
            todo = Todo.objects.get(pk=pk)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def get(self, request, pk:int):
        todo = self.get_object(pk=pk)
        print(pk)
        print(todo)
        todo_serialized = TodoSerializer(todo)
        return Response(todo_serialized.data, status.HTTP_200_OK)

    def put(self, request, pk:int):
        todo = self.get_object(pk=pk)
        todo_serialized = TodoSerializer(todo, data=request.data)
        if todo_serialized.is_valid():
            todo_serialized.save()
            return Response(todo_serialized.data, status.HTTP_200_OK)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk:int):
        todo = self.get_object(pk=pk)
        todo.delete()
        return Response(None, status.HTTP_200_OK)


# endregion

# region mixins

class TodoMixin(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request):
        return self.list(request)

    def post(self, request: Request):
        return self.create(request)


class TodoMixinDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request, pk):
        return self.retrieve(request, pk)

    def put(self, request: Request, pk):
        return self.update(request, pk)

    def delete(self, request: Request, pk):
        return self.destroy(request, pk)

# endregion

# region generics


class TodoGeneric(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer


class TodoGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
# endregion

# region viewsets


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
# endregion

#region usergeneric


class UserGeneric(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

#endregion

