from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.urls import reverse_lazy
from .models import Task


class CustomLoginView(LoginView):
    template_name= "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')

class Registerpage(FormView):
    template_name ='base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user=True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(Registerpage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('logout')
        return super(Registerpage, self).get(*args, **kwargs)
            

class TaskList(LoginRequiredMixin,ListView):
    model= Task
    context_object_name='tasklist'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tasklist']=context['tasklist'].filter(user=self.request.user)
        context['count']=context['tasklist'].filter(complete=False).count()

        if search_input := self.request.GET.get('search-area',) or '':
            context['tasklist']=context['tasklist'].filter(titles__startswith=search_input)
        context['search_input']=search_input

        return context
    

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    cotext_object_name='taskdetail'
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['titles','description','complete']  #'__all__' for all fields
    success_url=reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['titles','description','complete']
    success_url=reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name="task"
    success_url=reverse_lazy('tasks')