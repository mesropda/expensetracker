from django.urls import path
from .views import user_home_page, monthly_report, history, add_expense, edit_expense, submit_edit_expense, delete_expense

app_name = "expenses"
urlpatterns = [

    path('index', user_home_page, name='index'),
    path('monthly-report', monthly_report, name='monthly'),
    path('history', history, name='history'),
    path('add-expense/', add_expense, name='add-expense'),
    path('edit-expense/', edit_expense, name='edit-expense'),
    path('edit-expense/<int:pk>/', submit_edit_expense,
         name='submit-edit-expense'),
    path('delete-expense/', delete_expense, name='delete-expense')

]
