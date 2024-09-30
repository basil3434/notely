from django.shortcuts import render

from rest_framework.response import Response

from rest_framework import generics

from rest_framework.views import APIView

from notes.serializers import UserSerializer,TaskSerializer

from notes.models import User,Task

from rest_framework import authentication,permissions

from notes.permissions import OwnerOnly

from django.db.models import Count
# Create your views here.

class UserCreationView(generics.CreateAPIView):
    
    serializer_class=UserSerializer
    
class TaskListCreateView(generics.ListCreateAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    # def list(self, request, *args, **kwargs):
    #     qs=Task.objects.all()
    #     serializer_instance=

    def get_queryset(self):
        qs=Task.objects.filter(owner=self.request.user)
        if "category" in self.request.query_params:
            cat_value=self.request.query_params.get("category")
            qs=qs.filter(category=cat_value)
        if "priority" in self.request.query_params:
            pri_value=self.request.query_params.get("priority")
            qs=qs.filter(priority=pri_value)
        return qs
    
    
class TaskRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

class TaskSummaryAPIView(APIView):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        qs=Task.objects.filter(owner=request.user)
        category_summary=qs.values("category").annotate(count=Count('category'))
        status_summary=qs.values("status").annotate(count=Count('status'))
        priority_summary=qs.values("priority").annotate(count=Count('priority'))
        task_count=qs.count()
        context={
            "cateegory_summary":category_summary,
            "status_summary":status_summary,
            "priority_summary":priority_summary,
            "task_count":task_count
        }
        return Response(data=context)

class CategoryLIstView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Task.category_choices
        st={cat for tp in qs for cat in tp}

        return Response(data=st)


