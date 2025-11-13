# todo/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from todo.models import Task
from .serializers import TaskSerializer
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
            operation_summary="List all todos for the current user",
            responses={200: TaskSerializer(many=True)}             
                        )
    def get(self, request, *args, **kwargs):
        """
        List all the todo items for given requested user
        """
        todos = Task.objects.filter(user=request.user.id)
        serializer = TaskSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# ---------------------------------------
    @swagger_auto_schema(
            request_body=TaskSerializer,
            operation_summary="Create a new todo",
            responses={201 : openapi.Response("Created",TaskSerializer),
                       400: 'Bad Request - Invalid data'
                       },              
                        )
    def post(self, request, *args, **kwargs):
        """
        Create the Task with given todo data
        """
        data = {"title": request.data.get("title"), "user": request.user.id}
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return Task.objects.get(id=todo_id, user=user_id)
        except Task.DoesNotExist:
            return None
# ---------------------------------------       
    @swagger_auto_schema(
        operation_summary="Retrieve a specific todo item",
        responses={
            200: TaskSerializer,
            404: "Not Found - The todo item does not exist"
        }
    )
    def get(self, request, todo_id, *args, **kwargs):
        """
        Retrieves the Task with given todo_id
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
# ---------------------------------------
    # def post(self, request, todo_id, *args, **kwargs):
    #     """
    #     Updates the todo item with given todo_id if exists
    #     """
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response(
    #             {"res": "Object with todo id does not exists"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     data = {
    #         "title": request.data.get("title"),
    #         "completed": request.data.get("completed"),
    #         "user": request.user.id,
    #     }
    #     serializer = TaskSerializer(
    #         instance=todo_instance, data=data, partial=True
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------
    @swagger_auto_schema(
        operation_summary="Update a todo item",
        request_body=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: "Bad Request - Invalid data",
            404: "Not Found - The todo item does not exist"
        }
    )
    def put(self, request, todo_id, *args, **kwargs): 
        """
        Updates the todo item with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(
            instance=todo_instance, data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------
    @swagger_auto_schema(
        operation_summary="Delete a todo item",
        responses={
            204: "No Content - The item was successfully deleted",
            404: "Not Found - The todo item does not exist"
        }
    )
    def delete(self, request, todo_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        todo_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_204_NO_CONTENT)
