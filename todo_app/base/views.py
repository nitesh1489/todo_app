from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy
from .models import Task


class CustomLoginView(LoginView):
    template_name= "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin,ListView):
    model= Task
    context_object_name='tasklist'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasklist'].filter(user=self.request.user)
        context['count']=context['tasklist'].filter(complete=False).count()
        return context
    

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    cotext_object_name='taskdetail'
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['titles','description']   #'__all__' for all fields
    success_url=reverse_lazy('tasks')
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields="__all__"
    success_url=reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name="task"
    success_url=reverse_lazy('tasks')