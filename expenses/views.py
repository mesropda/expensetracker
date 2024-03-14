from .filters import TransactionFilter
from .models import Transactions
from tracker.views import check_if_user_loggedin
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import TransactionFrom, MonthlyTransactionsForm
from django.core.paginator import Paginator
import calendar
import datetime
import plotly.express as px


# Create your views here.

# view user dashbord function, also called index in urls.py

def user_home_page(request):
    user = check_if_user_loggedin(request)
    user_transactions = Transactions.objects.filter(user=user)
    todayDate = datetime.date.today()
    start_date = todayDate.replace(day=1)
    month_name = calendar.month_name[start_date.month]

    currentMonthExpenses = user_transactions.filter(date__year__gte=start_date.year,
                                                    date__month__gte=start_date.month)
    currentMonthTotal = 0
    for currentMonthExpense in currentMonthExpenses:
        currentMonthTotal += currentMonthExpense.amount

    context = {'form': TransactionFrom(),
               'transactions': user_transactions.order_by('-id')[:10],
               'current_month': currentMonthTotal,
               'month': month_name,
               'saving': user.savings}

    return render(request, "index.html", context)

# view monthly report page


def monthly_report(request):

    categories = {
        "House": 0,
        "Food": 0,
        "Transport": 0,
        "Shopping": 0,
        "Necessities": 0,
        "Bills": 0,
        "Leisure": 0,
        "Other": 0
    }
    '''Checki if the user is logged in, then filter throgh th transactions 
    according to motth which is beeing posted'''
    user = check_if_user_loggedin(request)
    if request.method == "POST":
        form = MonthlyTransactionsForm(request.POST)
        if form.is_valid() and form.cleaned_data['month'] != '--------':
            transactions = Transactions.objects.filter(
                user=user, date__month=form.cleaned_data['month'])
            month_number = int(form.cleaned_data['month'])
            month = calendar.month_name[month_number]

            if not transactions.exists():  # Check if there are records for the given month

                message = messages.success(request, "No records for "+month)
                return render(request, "monthly-report.html", {'form': form})

            '''Loop through categories and sum amount spend on each category during the specified month'''
            for key, value in categories.items():
                single_category_total = 0
                current_set = transactions.filter(category=key)
                for current in current_set:
                    single_category_total += current.amount
                    value = single_category_total
                categories[key] = single_category_total
            chart = piechart(categories, month)
            context = {'form': form, 'chart': chart}
        else:
            context = {'form': form}
    else:
        form = MonthlyTransactionsForm()
        context = {'form': form}
    return render(request, "monthly-report.html", context)


'''function to draw pie chart of manthly expenses in monthly report view
It acepts dictionary of categories and theyr corresponding amount during the month and 
return a cahrt in from of html'''


def piechart(categories, month):
    labels = categories.keys()
    sizes = categories.values()

    fig = px.pie(values=sizes, names=labels,
                 title=f'Expenses per category in {month}')

    fig.update_layout(title={'xanchor': 'center', 'x': 0.5},
                      width=810, height=810)
    fig.update_traces(textposition='inside',
                      textinfo='label+percent')

    chart = fig.to_html
    return chart


# view history page
def history(request):
    user = check_if_user_loggedin(request)
    transactions = Transactions.objects.filter(
        user=user)
    transactions_filtered = TransactionFilter(
        request.GET, queryset=transactions)
    paginator = Paginator(transactions_filtered.qs.order_by('-id'), 20)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {'form': transactions_filtered.form,
               'transactions': page_obj}
    return render(request, "history.html", context)

# function for adding a new expense in user_home_page view


def add_expense(request):
    if request.method == 'POST':
        user = check_if_user_loggedin(request)
        form = TransactionFrom(request.POST or None)
        if form.is_valid():
            new_transaction = Transactions(
                transaction_type=form.cleaned_data['transaction_type'], amount=form.cleaned_data['amount'], category=form.cleaned_data['category'], source=form.cleaned_data['source'])
            new_transaction.user = user
            new_transaction.save()
            context = {'transaction': new_transaction}
            return render(request, 'partials/transaction.html', context)
    return render(request, 'partials/form.html', {'form': TransactionFrom()})


def edit_expense(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        if len(selected_ids) != 0:
            selected_transactions = []
            form = TransactionFrom(request.POST or None)
            for id in selected_ids:
                obj = get_object_or_404(Transactions, pk=id)
                selected_transactions.append(obj)
            context = {'form': form, 'transactions': selected_transactions}
            return render(request, 'edit_expense.html', context)
        else:
            return history(request)


def submit_edit_expense(request, pk):
    obj = Transactions.objects.get(pk=pk)
    if request.method == 'POST':
        form = TransactionFrom(request.POST, instance=obj)
        print(obj.amount)
        if form.is_valid():
            form.save()
            context = {'transaction': obj}
            return render(request, 'partials/transaction.html', context)
    else:
        form = TransactionFrom()
    return render(request, 'partials/form_edit_expense.html', {'form': form})


def delete_expense(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        print(len(selected_ids))
        if len(selected_ids) != 0:
            for id in selected_ids:
                obj = get_object_or_404(Transactions, pk=id)
                obj.delete()
            return history(request)
        else:
            return history(request)


def vew_user_transactions(request):
    user = check_if_user_loggedin(request)
    context = {'transactions': Transactions.objects.filter(
        user=user).order_by('-id')}
    return render(request, "vew_transactions_template.html", context)
