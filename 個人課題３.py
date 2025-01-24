import requests
import flet as ft
import time

# API URL 定義
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/{base_currency}"

# 為替データを取得する関数
def fetch_exchange_rates(base_currency):
    try:
        url = EXCHANGE_API_URL.format(base_currency=base_currency)
        response = requests.get(url)
        response.raise_for_status()
        time.sleep(1)  # 過剰リクエストを防ぐための待機時間
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"為替データ取得エラー: {e}")
        return None

# 為替レートアプリ
def main(page: ft.Page):
    page.title = "為替レート表示アプリ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10

    # 為替レートカード作成
    def build_exchange_card(target_currency, rate):
        return ft.Card(
            content=ft.Column(
                [
                    ft.Text(target_currency, size=16, weight="bold", text_align="center"),
                    ft.Text(f"1 {base_currency_dropdown.value} = {rate:.2f} {target_currency}",
                            weight="bold",
                            text_align="center"),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            elevation=4,
            width=300,
            height=100,
        )

    # 為替レートを更新する
    def update_exchange_rates(e):
        selected_base_currency = base_currency_dropdown.value
        if not selected_base_currency:
            exchange_container.controls.append(
                ft.Text("基準通貨が選択されていません", color=ft.Colors.RED, size=20)
            )
            page.update()
            return

        exchange_data = fetch_exchange_rates(selected_base_currency)
        exchange_container.controls.clear()

        if not exchange_data:
            exchange_container.controls.append(
                ft.Text("為替データが取得できませんでした", color=ft.Colors.RED, size=20)
            )
            page.update()
            return

        rates = exchange_data.get("rates", {})
        for target_currency, rate in rates.items():
            if target_currency in target_currencies:
                exchange_container.controls.append(build_exchange_card(target_currency, rate))
        
        page.update()

    # 基準通貨と対象通貨の設定
    base_currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD"]
    target_currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CNY", "CHF", "INR"]

    base_currency_dropdown = ft.Dropdown(
        label="基準通貨を選択",
        options=[ft.dropdown.Option(key=code, text=code) for code in base_currencies],
        on_change=update_exchange_rates,
        width=300,
    )

    exchange_container = ft.Row(
        wrap=True, spacing=10, alignment=ft.MainAxisAlignment.START
    )

    # UI 構成
    page.add(
        ft.AppBar(
            title=ft.Text("為替レート表示アプリ", size=20, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.INDIGO,
        ),
        ft.Column(
            [base_currency_dropdown, ft.Container(content=exchange_container, padding=10)],
            alignment="start",
            spacing=20,
            scroll="auto",
        ),
    )

# アプリケーションを実行
ft.app(target=main)
