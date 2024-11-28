import flet as ft
import requests
import threading
import time
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime

# Configura Matplotlib para renderização apenas em arquivos
matplotlib.use("Agg")

# Função para buscar dados históricos de preços (últimas 24 horas)
def get_crypto_price_history(crypto_id, currency="usd"):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency={currency}&days=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta erro para status de resposta 4xx ou 5xx
        return response.json()  # Retorna o histórico de preços como dicionário
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Função para gerar o gráfico de variação de 24 horas
def generate_price_variation_chart(prices, filename):
    timestamps, variations = zip(*prices)  # Desempacota os dados para timestamps e variações
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, variations, label="24h Price Change (%)", color='blue')
    plt.xlabel("Timestamp")
    plt.ylabel("Price Change (%)")
    plt.title("Cryptocurrency Price Variation in 24 hours")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Função para atualizar o preço, variação de 24h e o gráfico
def update_price_and_change(selected_crypto_id, price_text, change_text, chart_image, page):
    # Faz a requisição para buscar o preço e a variação de 24 horas da criptomoeda selecionada
    prices = get_crypto_price_history(selected_crypto_id, "usd")
    if prices:
        price = prices.get('prices', [])[-1][1]  # Último preço
        price_change_percentage_24h = prices.get('prices', [])
        
        # Calcular a variação de preço nas últimas 24 horas (percentual)
        variations = [(datetime.fromtimestamp(t[0] / 1000).strftime('%H:%M:%S'), t[1]) for t in price_change_percentage_24h]
        
        # Atualizar o gráfico com a variação
        generate_price_variation_chart(variations, "chart.png")
        
        # Atualizar os textos de preço e variação
        price_text.value = f"{selected_crypto_id.capitalize()}: ${price:.2f}"
        change_text.value = f"24h Change: {variations[-1][1]:.2f}%"
        chart_image.src = "chart.png"  # Atualiza a imagem do gráfico
        
    else:
        price_text.value = f"Failed to fetch price for {selected_crypto_id.capitalize()}"
        change_text.value = "24h Change: N/A"
        chart_image.src = ""  # Se falhar, não exibe o gráfico

    page.update()

# Função para atualização contínua em thread
def start_auto_update(selected_crypto_id, price_text, change_text, chart_image, page):
    while True:
        update_price_and_change(selected_crypto_id, price_text, change_text, chart_image, page)  # Atualiza o preço, a variação e o gráfico
        time.sleep(10)  # Atualiza a cada 10 segundos

# Função principal do Flet
def main(page: ft.Page):
    page.title = "Crypto Prices Tracker with 24h Chart"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Lista de criptomoedas a serem monitoradas
    crypto_list = [
        {"id": "bitcoin", "name": "Bitcoin"},
        {"id": "ethereum", "name": "Ethereum"},
        {"id": "solana", "name": "Solana"},
        {"id": "bitcoin-cash", "name": "Bitcoin Cash"},
        {"id": "litecoin", "name": "Litecoin"},
        {"id": "ripple", "name": "Ripple"},
        {"id": "cardano", "name": "Cardano"},
        {"id": "polkadot", "name": "Polkadot"},
        {"id": "binancecoin", "name": "Binance Coin"},
        {"id": "dogecoin", "name": "Dogecoin"},
        {"id": "chainlink", "name": "Chainlink"},
        {"id": "uniswap", "name": "Uniswap"},
        {"id": "shiba-inu", "name": "Shiba Inu"},
        {"id": "avalanche-2", "name": "Avalanche"},
    ]

    # Dicionário para armazenar o texto que será exibido
    price_text = ft.Text("Select a cryptocurrency to view price...", size=25, weight=ft.FontWeight.BOLD)
    change_text = ft.Text("24h Change: N/A", size=20, weight=ft.FontWeight.NORMAL)
    
    # Imagem do gráfico
    chart_image = ft.Image(src="", width=600, height=400)

    # Função para tratar a seleção do dropdown
    def on_dropdown_change(e):
        selected_crypto_id = e.control.value
        price_text.value = f"Fetching price for {selected_crypto_id.capitalize()}..."
        change_text.value = "Fetching 24h change..."
        page.update()
        
        # Inicia a atualização contínua em thread
        threading.Thread(target=start_auto_update, args=(selected_crypto_id, price_text, change_text, chart_image, page), daemon=True).start()

    # Dropdown com as criptomoedas
    crypto_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(crypto["id"], text=crypto["name"]) for crypto in crypto_list
        ],
        label="Select Cryptocurrency",
        on_change=on_dropdown_change,
    )

    # Adiciona o dropdown, os textos e o gráfico na página
    page.add(
        ft.Column(
            [
                crypto_dropdown,
                price_text,
                change_text,
                chart_image,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)
