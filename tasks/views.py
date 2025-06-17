from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.timezone import now
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        due = self.request.GET.get('due')
        overdue = self.request.GET.get('overdue')
        created = self.request.GET.get('created')

        if status == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif status == 'pending':
            queryset = queryset.filter(is_completed=False)

        if priority:
            queryset = queryset.filter(priority=priority)

        if due:
            queryset = queryset.filter(due_date=due)

        if overdue == 'true':
            queryset = queryset.filter(is_completed=False, due_date__lt=now().date())

        if created:
            queryset = queryset.filter(created_at__date=created)

        return queryset.order_by('-created_at')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm  # ✅ FIXED: changed from `fields = TaskForm`
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit.html'
    success_url = reverse_lazy('home')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')
    template_name = 'tasks/confirm_delete.html'


@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
