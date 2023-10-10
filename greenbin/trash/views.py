from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from datetime import datetime,timedelta
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

from trash.forms import TrashForm
from food.models import Food
from trash.models import Trash
from user.models import Profile

# Create your views here.
@login_required(login_url="/login")
def home(request):
    past_process = Trash.objects.all().filter(user=request.user)
    profile = request.user.profile
    food_list = Food.objects.all().filter(category=7)
    query = Trash.objects.all().filter(user=request.user, on_process=True)
    if query:
        current_process = query[0]
    else:
        current_process = False
    if request.method == 'POST' and not current_process:
        form = TrashForm(request.POST)
        if form.is_valid():
            trash = form.save(commit=False)

            trash.user = request.user
            trash.on_process = True
            trash.start_date = datetime.now()
            trash.start_date_formated = datetime.now().strftime(("%m/%d/%Y %H:%M:%S"))

            aux_size = request.POST['user_size']
            aux_duration = request.POST['user_duration']

            if aux_duration and aux_size:
                trash.user_size = float(aux_size)
                trash.user_duration = timedelta(hours=int(aux_duration.split(":")[0]), minutes=int(aux_duration.split(":")[1]),seconds=int(aux_duration.split(":")[2]))
                trash.duration = trash.user_duration
                if trash.user_size < 200:
                    trash.size = "S"
                if 200 < trash.user_size < 350:
                    trash.size = "M"
                if 350 < trash.user_size:
                    trash.size = "L"

            if aux_duration and not aux_size:
                trash.user_duration = timedelta(hours=int(aux_duration.split(":")[0]), minutes=int(aux_duration.split(":")[1]),seconds=int(aux_duration.split(":")[2]))
                trash.duration = trash.user_duration
                if trash.size == "S":
                    trash.user_size = 150.00
                if trash.size == "M":
                    trash.user_size = 275.00
                if trash.size == "L":
                    trash.user_size = 425.00

            if not aux_duration and aux_size:
                trash.user_size = float(aux_size)
                if trash.user_size < 200:
                    trash.size = "S"
                    trash.duration = timedelta(hours=6)
                if 200 < trash.user_size < 350:
                    trash.size = "M"
                    trash.duration = timedelta(hours=8)
                if 350 < trash.user_size:
                    trash.size = "L"
                    trash.duration = timedelta(hours=10)
                trash.user_duration = trash.duration

            if not aux_duration and not  aux_size:
                if trash.size == "S":
                    trash.duration = timedelta(hours=6)
                    trash.user_size = 150.00
                if trash.size == "M":
                    trash.duration = timedelta(hours=8)
                    trash.user_size = 275.00
                if trash.size == "L":
                    trash.user_size = 425.00
                    trash.duration = timedelta(hours=10)
                trash.user_duration = trash.duration

            trash.end_date = trash.start_date + trash.duration
            trash.processed_size =  trash.user_size * 0.4214

            trash.save()
            profile.processes.add(trash)
            form.save_m2m()
            duration = trash.user_duration
            seconds = duration.seconds
            return redirect('trash:process', pk=trash.id, seconds=seconds)
    else:
        form = TrashForm()

    return render(request, 'trash/home.html', {'form': form, 'not_foods':food_list, 'past_processes':past_process, 'current_process': current_process},)

@login_required(login_url="/login")
def process(request, pk, seconds):
    trash = get_object_or_404(Trash, id=pk, user=request.user)
    return render(request, 'trash/trash_process.html', {'trash':trash})

@login_required(login_url="/login")
def process_completed(request, pk):
    trash = get_object_or_404(Trash, id=pk, user=request.user)
    trash.on_process = False
    trash.save()
    return render(request, 'trash/trash_process.html', {'trash':trash})

class TrashList(LoginRequiredMixin, ListView):
    model = Trash
    queryset = Trash.objects.order_by('id')
    context_object_name = 'trashes'

    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        order = self.request.GET.get('order')
        if filter_val:
            if order == "asc":
                new_context = Trash.objects.filter(user=self.request.user).order_by(filter_val)
            else:
                query = "-" + filter_val
                new_context = Trash.objects.filter(user=self.request.user).order_by(query)
        else:
            new_context = Trash.objects.filter(user=self.request.user)
        return new_context

class TrashDetail(LoginRequiredMixin, DetailView):
    model = Trash

class TrashDelete(LoginRequiredMixin, DeleteView):
    model = Trash
    success_url = reverse_lazy('trash:all')

class TrashUpdate(LoginRequiredMixin, UpdateView):
    model = Trash
    fields = ["end_date","duration","size", "foods"]
    template_name_suffix = "_update_form"

def jsonProcess(request):
    query = Trash.objects.all().filter(on_process=True)
    if query:
        print(query)
        current_process = query[0]
        duration = current_process.user_duration
        seconds = duration.seconds
        print(seconds)
        data = {
            'ID': current_process.id,
            'duration': seconds
        }
        response = JsonResponse(data, status=200)
        return response
    else:
        return HttpResponseNotFound("PAGE NOT FOUND")