from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView

from .models import Task


# Create your views here.

# mixins -->builtin classes in django which can be inherited for easier use

#  Listing of Task

def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterView, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task  # model that is used
    context_object_name = 'task'  # variable name in template context(making user friendly)
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(completed=False).count()
    #
    #     search_input = self.request.GET.get('search-area') or ''
    #     if search_input:
    #         context['task'] = context['task'].filter(title__starswith=search_input)
    #
    #     context['search_input'] = search_input
    #
        return context



class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task')
    template_name = 'taskcreate.html'

    def form_valid(self, form):  # to validate form based on object and user
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task')
    template_name = 'taskcreate.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task')
    template_name = 'taskdelete.html'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'taskdetail.html'
