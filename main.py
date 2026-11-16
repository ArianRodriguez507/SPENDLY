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
    page.bgcolor = "#FFD6E7"
    page.padding = 20

    transactions = load_data()

    title = ft.Text(
        "💰 SPENDLY",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#C2185B",
    )

    subtitle = ft.Text(
        "Manage your money smarter with Spendly",
        size=16,
        color=ft.Colors.GREY,
    )

    balance_text = ft.Text(
        "$0.00",
        size=24,
        weight=ft.FontWeight.BOLD,
    )

    income_text = ft.Text(
        "$0.00",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN,
    )

    expense_text = ft.Text(
        "$0.00",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED,
    )

    message = ft.Text("", color=ft.Colors.RED)

    description = ft.TextField(
        label="Description",
        width=280,
    )

    amount = ft.TextField(
        label="Amount",
        width=180,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    category = ft.Dropdown(
        label="Category",
        width=280,
        value="Other",
        options=[
            ft.dropdown.Option("Food"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("School"),
            ft.dropdown.Option("Entertainment"),
            ft.dropdown.Option("Other"),
        ],
    )

    dark_mode = ft.Switch(label="Dark Mode")

    transaction_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
    )

    def update_balance():

        total = sum(
            item["amount"]
            for item in transactions
        )

        income = sum(
            item["amount"]
            for item in transactions
            if item["amount"] > 0
        )

        expenses = abs(
            sum(
                item["amount"]
                for item in transactions
                if item["amount"] < 0
            )
        )

        balance_text.value = f"${total:.2f}"
        income_text.value = f"${income:.2f}"
        expense_text.value = f"${expenses:.2f}"

        if total > 0:
            balance_text.color = ft.Colors.GREEN
        elif total < 0:
            balance_text.color = ft.Colors.RED
        else:
            balance_text.color = ft.Colors.BLUE

    def refresh_transactions():

        transaction_list.controls.clear()

        for item in transactions:

            if item["category"] == "Food":
                icon_color = ft.Colors.ORANGE
            elif item["category"] == "Transport":
                icon_color = ft.Colors.BLUE
            elif item["category"] == "School":
                icon_color = ft.Colors.PURPLE
            elif item["category"] == "Entertainment":
                icon_color = ft.Colors.PINK
            else:
                icon_color = ft.Colors.GREY

            amount_color = (
                ft.Colors.GREEN
                if item["amount"] >= 0
                else ft.Colors.RED
            )

            transaction_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.PAYMENTS,
                        color=icon_color,
                    ),
                    title=ft.Text(item["description"]),
                    subtitle=ft.Text(item["category"]),
                    trailing=ft.Text(
                        f"${item['amount']:.2f}",
                        color=amount_color,
                    ),
                )
            )

        update_balance()
        page.update()

    def clear_fields():
        description.value = ""
        amount.value = ""

    def add_income(e):
        try:

            value = float(amount.value)

            transactions.append(
                {
                    "description": description.value,
                    "amount": value,
                    "category": category.value,
                }
            )

            save_data(transactions)

            clear_fields()
            message.value = ""

            refresh_transactions()

        except:
            message.value = "Enter a valid amount."
            page.update()

    def add_expense(e):
        try:

            value = float(amount.value)

            transactions.append(
                {
                    "description": description.value,
                    "amount": -value,
                    "category": category.value,
                }
            )

            save_data(transactions)

            clear_fields()
            message.value = ""

            refresh_transactions()

        except:
            message.value = "Enter a valid amount."
            page.update()

    def clear_history(e):

        transactions.clear()

        save_data(transactions)

        refresh_transactions()

    income_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("💵 Income"),
                income_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#D4F8D4",
        border_radius=15,
        padding=15,
        width=180,
    )

    expense_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("💸 Expenses"),
                expense_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#FFD6D6",
        border_radius=15,
        padding=15,
        width=180,
    )

    balance_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("💰 Balance"),
                balance_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#D6E4FF",
        border_radius=15,
        padding=15,
        width=180,
    )

    main_card = ft.Container(
        width=800,
        bgcolor="#FFF0F6",
        border_radius=30,
        padding=30,
        content=ft.Column(
            [
                title,
                subtitle,
                dark_mode,

                ft.Row(
                    [
                        balance_card,
                        income_card,
                        expense_card,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Divider(),

                ft.Row(
                    [
                        description,
                        amount,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                category,

                message,

                ft.Row(
                    [
                        ft.Button(
                            "💵 Add Income",
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            on_click=add_income,
                        ),

                        ft.Button(
                            "💸 Add Expense",
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            on_click=add_expense,
                        ),

                        ft.Button(
                            "🗑 Clear History",
                            bgcolor=ft.Colors.ORANGE,
                            color=ft.Colors.WHITE,
                            on_click=clear_history,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Divider(),

                ft.Text(
                    "📋 Transaction History",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                transaction_list,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    def change_theme(e):

        if dark_mode.value:

            page.theme_mode = ft.ThemeMode.DARK

            page.bgcolor = "#1A1A1A"
            main_card.bgcolor = "#2D2D2D"

            title.color = "#F48FB1"
            subtitle.color = ft.Colors.WHITE

        else:

            page.theme_mode = ft.ThemeMode.LIGHT

            page.bgcolor = "#FFD6E7"
            main_card.bgcolor = "#FFF0F6"

            title.color = "#C2185B"
            subtitle.color = ft.Colors.GREY

        page.update()

    dark_mode.on_change = change_theme

    page.add(
        ft.Row(
            [main_card],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    refresh_transactions()


ft.run(main)