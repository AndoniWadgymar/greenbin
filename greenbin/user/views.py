import datetime
import calendar
from datetime import timedelta

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from user.models import Profile
from trash.models import Trash
from user.forms import UserUpdateForm,ProfileUpdateForm

# Create your views here.
@login_required(login_url="/login")
def profile(request):
    filterg = str(request.GET.get('filter'))
    typeg = str(request.GET.get('type'))
    today = datetime.datetime.now()
    profile = Profile.objects.get(user=request.user)
    processes_data = []
    processes_date = []

    if filterg == "day":
        processes = profile.processes.all().filter(start_date__day=today.day, start_date__month=today.month, start_date__year=today.year)
        for process in processes:
            if typeg == "duration":
                processes_data.append(process.duration.seconds/3600)
            else: 
                processes_data.append(process.user_size)
            processes_date.append(process.start_date)

    if filterg == "week":
        # for i in range(0,8):
        #     day = str(datetime.datetime.now() - timedelta(days=i))
        #     print(day[0:10])
        #     if typeg == "duration":
        #         day_data = profile.processes.all().filter(start_date__day=6).aggregate(total=Sum('duration'))['total']
        #         print(day_data)
        #         if day_data:
        #             days = day_data.days * 24 
        #             seconds = day_data.seconds /3600
        #             total = days + seconds
        #             day_data = total
        #     else:
        #         day_data = profile.processes.all().filter(start_date__day=6).aggregate(total=Sum('user_size'))['total']

        today = str(datetime.datetime.now() + timedelta(days=1))
        back = str(datetime.datetime.today() - timedelta(days=7))
        week_processes = profile.processes.all().filter(start_date__gte=back[0:10], start_date__lte=today[0:10]).order_by("start_date")
        process_dict = {}
        for process in week_processes:
            date = str(process.start_date)[0:10]
            if date in process_dict:
                if typeg == "duration":
                    process_dict[date] += (process.duration.seconds/3600)
                else:
                    process_dict[date] += process.user_size
            else:
                if typeg == "duration":
                    process_dict[date] = (process.duration.seconds/3600)
                else:
                    process_dict[date] = process.user_size
        processes_data = process_dict.values()
        processes_date = process_dict.keys()

    if filterg == "month":
        for i in range(0,12):
            if typeg == "duration":
                month_data = profile.processes.all().filter(start_date__month=i+1).aggregate(total=Sum('duration'))['total']
                if month_data:
                    days = month_data.days * 24 
                    seconds = month_data.seconds /3600
                    total = days + seconds
                    month_data = total
            else:
                month_data = profile.processes.all().filter(start_date__month=i+1).aggregate(total=Sum('user_size'))['total']
            processes_data.append(month_data)
            processes_date.append(calendar.month_name[i+1])
    
    if filterg == "year":
        current_year = int(today.year)
        for i in range(current_year-10,current_year+1):
            if typeg == "duration":
                year_data = profile.processes.all().filter(start_date__year=i).aggregate(total=Sum('duration'))['total']
                if year_data:
                    days = year_data.days * 24 
                    seconds = year_data.seconds /3600
                    total = days + seconds
                    year_data = total
            else:
                year_data = profile.processes.all().filter(start_date__year=i).aggregate(total=Sum('user_size'))['total']
            processes_data.append(year_data)
            processes_date.append(i)
    
    all_trashes = Trash.objects.all().filter(user=request.user)
    all_foods = [trash.foods.all().values_list('name','category_id') for trash in all_trashes]
    
    food_fruit_dict = {}
    food_vegetable_dict = {}
    food_grain_dict = {}
    food_dairy_dict = {}
    food_protein_dict = {}
    food_other_dict = {}

    for food in all_foods:
        for i in range(len(food)):
            name = food[i][0]
            category = food[i][1]
            if category == 1:
                if name in food_fruit_dict:
                    food_fruit_dict[name] +=1
                else:
                    food_fruit_dict[name] = 1
            if category == 2:
                if name in food_vegetable_dict:
                    food_vegetable_dict[name] +=1
                else:
                    food_vegetable_dict[name] = 1
            if category == 3:
                if name in food_dairy_dict:
                    food_dairy_dict[name] +=1
                else:
                    food_dairy_dict[name] = 1
            if category == 4:
                if name in food_grain_dict:
                    food_grain_dict[name] +=1
                else:
                    food_grain_dict[name] = 1
            if category == 5:
                if name in food_protein_dict:
                    food_protein_dict[name] +=1
                else:
                    food_protein_dict[name] = 1
            if category == 6:
                if name in food_other_dict:
                    food_other_dict[name] +=1
                else:
                    food_other_dict[name] = 1
            
    food_fruit_data = food_fruit_dict.values()
    food_fruit_name = food_fruit_dict.keys()
    food_vegetable_data = food_vegetable_dict.values()
    food_vegetable_name = food_vegetable_dict.keys()
    food_dairy_data = food_dairy_dict.values()
    food_dairy_name = food_dairy_dict.keys()
    food_grain_data = food_grain_dict.values()
    food_grain_name = food_grain_dict.keys()
    food_protein_data = food_protein_dict.values()
    food_protein_name = food_protein_dict.keys()
    food_other_data = food_other_dict.values()
    food_other_name = food_other_dict.keys()

    return render(request, 'user/user_detail.html', {'processes_data_list':processes_data, 
                                                     'processes_date_list':processes_date, 
                                                     'food_fruit_data_list':food_fruit_data,
                                                     'food_fruit_name_list':food_fruit_name,
                                                     'food_vegetable_data_list':food_vegetable_data,
                                                     'food_vegetable_name_list':food_vegetable_name,
                                                     'food_dairy_data_list':food_dairy_data,
                                                     'food_dairy_name_list':food_dairy_name,
                                                     'food_grain_data_list':food_grain_data,
                                                     'food_grain_name_list':food_grain_name,
                                                     'food_protein_data_list':food_protein_data,
                                                     'food_protein_name_list':food_protein_name,
                                                     'food_other_data_list':food_other_data, 
                                                     'food_other_name_list':food_other_name,  })

@login_required(login_url="/login")
def update_profile(request):
    
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user:profile')
    else:  
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'user/user_update.html',{'user_form':user_form, 'profile_form':profile_form})