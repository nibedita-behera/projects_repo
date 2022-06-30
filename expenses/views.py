from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Status, Expense
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import datetime


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            cost__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            status__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    status = Status.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    status = Status.objects.all()
    context = {
        'status': status,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        cost = request.POST['cost']

        if not cost:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        name=request.POST['name']
        description = request.POST['description']
        date = request.POST['expense_date']
        status = request.POST['status']

        if not name:
            messages.error(request, 'name is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, name=name, cost=cost, date=date,
                               status=status, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    status = Status.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'status': status
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        cost = request.POST['cost']

        if not cost:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        name=request.POST['name']
        description = request.POST['description']
        date = request.POST['expense_date']
        status = request.POST['status']

        if not name:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.cost = cost
        expense. date = date
        expense.status = status
        expense.description = description
        expense.name=name

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')




def stats_view(request):
    data=Expense.objects.all()
    context={
        'data':data
    }   
    return render(request, 'expenses/stats.html',context)

def date_view(request):
    data=Expense.objects.all()
    context={
        'data':data
    }   
    return render(request, 'expenses/date_chart.html',context)
def status_view(request):
    data=Expense.objects.all()
    context={
        'data':data
    }   
    return render(request, 'expenses/status_chart.html',context)