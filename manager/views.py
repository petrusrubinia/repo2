import json

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response

from manager.constants import TaskState
from manager.models import Task, Board
from manager.serializers import TaskSerializer
'''
@csrf_exempt
def list_tasks(request):
    """Return a JsonResponse with all Task records in the database"""
    # We list the Tasks only if the HTTP method is GET
    # What do we do when a POST comes in?
    if request.method == 'GET':
        # create a queryset for all the records from the Task model
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        # transform each task into a dict representation and add it to a list
        dict_tasks = []
        for task in tasks:
            # add the other fields from `task` here
            task_dict = {
                'id': task.id,
                'name': task.name,
                'description': task.description
            }
            dict_tasks.append(task_dict)

        # return a JSON response (sets content type to "application/json")
        return JsonResponse(dict_tasks, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(
            name=data['name'],
            description=data['description'],
            state=data['state'],
        )
        return JsonResponse({}, status=200)


def get_board(request, pk):
    # We return the details of a single item when the HTTP method is GET
    if request.method == 'GET':
        try:
            # We try to retrieve the object with the given pk
            board = Board.objects.get(id=pk)
        except Board.DoesNotExist:
            # If we get an exception, namely DoesNotExist, we return a 404
            return JsonResponse({'detail': 'Not found'}, status=404)

        dict_board = {
            'id': board.id,
            'name': board.name
        }
        return JsonResponse(dict_board)


'''

from rest_framework import viewsets

from manager.serializers import TaskSerializer, BoardSerializer
from manager.models import Task


# Instead of having two views for working with Tasks, we can have only one, a
# smart one
# This view can deal with all the responsibilities of the prior two views, combined
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=False, methods=['GET'])
    def done_tasks(self,request):
        queryset = Task.objects.filter(state=TaskState.DONE)
        serializer = TaskSerializer(queryset,many=True)

        return Response(serializer.data)

    def filter_queryset(self, queryset):
        board = self.request.GET.get('board')
        if board:
            queryset = queryset.filter(board=board)
        return queryset

class BoardViewSet(viewsets.ModelViewSet):

    serializer_class =  BoardSerializer
    queryset = Board.objects.all()

