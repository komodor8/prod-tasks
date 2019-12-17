from .models import Task, TaskForm, Comment, CommentForm, TaskShareForm
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import ModelFormMixin

# Create your views here.


class IndexTaskView(LoginRequiredMixin, ListView):
    template_name = 'tasks/index.html'
    model = Task

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id).prefetch_related('user')


class DetailTaskView(LoginRequiredMixin, DetailView):
    template_name = 'tasks/detail.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user != self.object.user:
            raise PermissionDenied
        form = CommentForm()
        context['comment_form'] = form
        context['users'] = User.objects.all()
        context['invited_users'] = self.object.invited.all()
        context['invited_users_form'] = TaskShareForm(instance=self.object)
        return context


class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    model = Task

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            messages.success(self.request, 'Your task has been added.')
        except:
            messages.warning(self.request, 'Oups ! Your task hasn\'t been added.')

        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        messages.success(self.request, 'Task has been updated.')
        return super().get_success_url()


class ShareTaskView(LoginRequiredMixin, UpdateView):
    form_class = TaskShareForm
    model = Task

    def get_success_url(self):
        messages.success(self.request, 'Task has been shared.')
        task_id = self.kwargs['pk']
        return str(reverse_lazy('tasks:detail', kwargs={'pk': task_id}))


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:index')

    def get_success_url(self):
        messages.success(self.request, 'Task has been deleted.')
        return super().get_success_url()


#################################################
#################################################


class CreateCommentView(LoginRequiredMixin, PermissionRequiredMixin, ModelFormMixin, FormView):
    template_name = 'tasks/detail.html'
    form_class = CommentForm
    model = Comment
    permission_denied_message = 'Who do you think you are ? Ask Jesus to move your priviligies up !!'
    permission_required = 'tasks.add_comment'

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.task_id = self.kwargs['task']
            self.object.save()
            messages.success(self.request, 'Your comment has been added.')
        except:
            messages.warning(self.request, 'Oups ! Your comment hasn\'t been added.')

        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, self.permission_denied_message)
            return redirect('tasks:detail', pk=self.kwargs['task'])
        return super().handle_no_permission()

    def get_success_url(self):
        task_id = self.kwargs['task']
        return str(reverse_lazy('tasks:detail', kwargs={'pk': task_id}))


class DeleteCommentView(DeleteView):
    model = Comment

    def get_success_url(self):
        task_id = self.kwargs['task']
        messages.success(self.request, 'Comment has been deleted.')
        return str(reverse_lazy('tasks:detail', kwargs={'pk': task_id}))


class UpdateCommentView(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        task_id = self.kwargs['task']
        messages.success(self.request, 'Comment has been updated.')
        return str(reverse_lazy('tasks:detail', kwargs={'pk': task_id}))
