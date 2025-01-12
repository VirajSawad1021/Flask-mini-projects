from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import Expense
from app.forms import ExpenseForm
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Add Expense Route
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        # Create a new expense entry
        expense = Expense(
            name=form.name.data,
            category=form.category.data,
            amount=form.amount.data,
            date=form.date.data
        )
        # Save the expense to the database
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html', form=form)

# View Expenses Route
@app.route('/expenses')
def view_expenses():
    # Fetch all expenses from the database
    expenses = Expense.query.all()
    return render_template('view_expenses.html', expenses=expenses)

# Report Visualization Route
@app.route('/report')
def report():
    # Fetch all expenses from the database
    expenses = Expense.query.all()
    
    # Check if there are any expenses
    if not expenses:
        flash('No expenses available to generate a report.', 'info')
        return render_template('report.html', chart_image=None)

    # Group expenses by category
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    # Generate a bar chart
    categories = list(category_totals.keys())
    totals = list(category_totals.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, totals, color='skyblue')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.tight_layout()
    
    # Save the chart to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    # Render the report page with the chart image
    return render_template('report.html', chart_image=chart_image)