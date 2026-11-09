import flet as ft
import json
import os

DATA_FILE = "expenses.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def main(page: ft.Page):

    page.title = "Spendly"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    transactions = load_data()

    title = ft.Text(
        "💰 Spendly Budget Tracker",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    balance_text = ft.Text(
        "Balance: $0.00",
        size=22,
        weight=ft.FontWeight.BOLD,
    )

    message = ft.Text(
        "",
        color=ft.Colors.RED,
    )

    description = ft.TextField(
        label="Description",
        width=250,
    )

    amount = ft.TextField(
        label="Amount",
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    category = ft.Dropdown(
        label="Category",
        width=220,
        value="Other",
        options=[
            ft.dropdown.Option("Food"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("School"),
            ft.dropdown.Option("Entertainment"),
            ft.dropdown.Option("Other"),
        ],
    )

    dark_mode = ft.Switch(
        label="Dark Mode"
    )

    transaction_list = ft.Column(
        scroll=ft.ScrollMode.AUTO
    )

    def update_balance():

        total = sum(
            item["amount"]
            for item in transactions
        )

        balance_text.value = (
            f"Balance: ${total:.2f}"
        )

        if total > 0:
            balance_text.color = ft.Colors.GREEN
        elif total < 0:
            balance_text.color = ft.Colors.RED
        else:
            balance_text.color = ft.Colors.BLUE

    def refresh_transactions():

        transaction_list.controls.clear()

        for item in transactions:

            color = (
                ft.Colors.GREEN
                if item["amount"] >= 0
                else ft.Colors.RED
            )

            transaction_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.PAYMENTS,
                        color=color,
                    ),
                    title=ft.Text(
                        item["description"]
                    ),
                    subtitle=ft.Text(
                        item["category"]
                    ),
                    trailing=ft.Text(
                        f"${item['amount']:.2f}",
                        color=color,
                    ),
                )
            )

        update_balance()
        page.update()

    def clear_fields():

        description.value = ""
        amount.value = ""

    def add_income(e):

        if not description.value:
            message.value = (
                "Please enter a description."
            )
            page.update()
            return

        try:

            value = float(amount.value)

            transactions.append(
                {
                    "description":
                    description.value,
                    "amount": value,
                    "category":
                    category.value,
                }
            )

            save_data(transactions)

            clear_fields()

            message.value = ""

            refresh_transactions()

        except ValueError:

            message.value = (
                "Enter a valid amount."
            )

            page.update()

    def add_expense(e):

        if not description.value:
            message.value = (
                "Please enter a description."
            )
            page.update()
            return

        try:

            value = float(amount.value)

            transactions.append(
                {
                    "description":
                    description.value,
                    "amount": -value,
                    "category":
                    category.value,
                }
            )

            save_data(transactions)

            clear_fields()

            message.value = ""

            refresh_transactions()

        except ValueError:

            message.value = (
                "Enter a valid amount."
            )

            page.update()

    def change_theme(e):

        if dark_mode.value:
            page.theme_mode = (
                ft.ThemeMode.DARK
            )
        else:
            page.theme_mode = (
                ft.ThemeMode.LIGHT
            )

        page.update()

    dark_mode.on_change = change_theme

    income_button = ft.Button(
        "Add Income",
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        on_click=add_income,
    )

    expense_button = ft.Button(
        "Add Expense",
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
        on_click=add_expense,
    )

    page.add(
        ft.Column(
            [
                title,
                balance_text,
                dark_mode,

                ft.Row(
                    [
                        description,
                        amount,
                    ]
                ),

                category,

                message,

                ft.Row(
                    [
                        income_button,
                        expense_button,
                    ]
                ),

                ft.Divider(),

                ft.Text(
                    "Transaction History",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                transaction_list,
            ]
        )
    )

    refresh_transactions()


ft.run(main)