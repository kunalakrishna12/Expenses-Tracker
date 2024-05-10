from expense import Expense
import calendar
import datetime
import os
    
def get_budget_for_month():
    current_month_year = f"{datetime.datetime.now().strftime('%Y-%m')}"
    budget_file_path = f"budget_{current_month_year}.txt"

    if os.path.exists(budget_file_path):
        with open(budget_file_path, 'r') as file:
            budget = float(file.read())
    else:
        budget = float(input("💲Enter Your Budget for the month: "))
        with open(budget_file_path, 'w') as file:
            file.write(str(budget))

    return budget

def main():
    print(f"🎸 Running Expense Tracker!")
    expense_file_path="expenses.csv"
    budget=get_budget_for_month()
    
    # Get user input for expense.
    expenses = get_user_expense()
    
    # Write their expense to a file
    for expense in expenses:    
        save_expense_to_file(expense , expense_file_path)
    
    # Read file and summarise expenses.
    summarize_user_expense(expense_file_path, budget)
    
     # Ask user for any additional budget

def get_user_expense():
    print(f"🎸 Getting User Expense")
    expenses = []
    while True:
        expense_name = input("Enter Expense name (or type 'done' to finish adding expenses):")

        if expense_name.lower() == 'done':
            break
        
        expense_amount = float(input("Enter Expense amount:"))
        
        expense_categories = [
            "🍕FOOD",
            "🏠HOME",
            "🏢WORK",
            "🕺FUN",
            "⭐MISC"
        ]
        
        while True:
            print("Select a Category:")
            for i,category_name in enumerate(expense_categories):
                print(f"  {i + 1}. {category_name}")
            selected_index = int(input("Enter a category number: "))
            
            if 1 <= selected_index <= len(expense_categories):
                selected_category = expense_categories[selected_index - 1]
                break
            else:
                print("Invalid category number. Please try again!")
        
        new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
        expenses.append(new_expense)

    return expenses
def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎸 Saving User Expense: {expense} to {expense_file_path} ")
    with open(expense_file_path,"a", encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
        
def summarize_user_expense(expense_file_path, budget ):
    print(f"🎸Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path,"r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            try:
                expense_name,expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(
                    name=expense_name, category=expense_category, amount=float(expense_amount)
                )
                expenses.append(line_expense)
            except ValueError:
                print(f"Skipping invalid line: {line}")

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f" {key}: {amount:.2f}rs")
        
    total_spent = sum([ex.amount for ex in expenses])
    print(f"💰Total Spent: {total_spent:.2f}rs")

    remaining_budget = budget - total_spent
    print(f"🔒Budget Remaining: {remaining_budget:.2f}rs")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year,now.month)[1]
    remaining_days = days_in_month - now.day
    print(f"📆Remaining Days in the current month {remaining_days}")
    
    daily_budget = remaining_budget / remaining_days
    print(green(f"👉Budget Per Day: {daily_budget:.2f}rs"))
    
    additional_budget = input("Would you like to add any additional budget? (yes/no): ")
    if additional_budget.lower() == "yes":
        additional_amount = float(input("Enter the additional budget amount: "))
        budget = remaining_budget + additional_amount
        print(f"Your updated budget is now: {budget}rs")

def green(text):
    return f"\033[92m{text}\033[0m"
if __name__=="__main__":
    main()
