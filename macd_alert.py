
# Script Python pour détecter un croisement MACD en 1H et envoyer une alerte email et une alerte de prix

import requests
import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration de l'URL du pool sur GeckoTerminal
POOL_URL = "https://api.geckoterminal.com/api/v2/networks/solana/pools/y2AVy9v4VgtCy2FEa5HqVEopRqydXsm2bzaG6Y9hsHs"

# Configuration de l'email d'alerte
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "lux.antoine.oculus"
EMAIL_PASSWORD = "e73ecPYNj6U8^NE5eHKZ"
TO_EMAIL = "ayka.lux@gmail.com"

# Niveau de prix pour l'alerte que l'utilisateur peut configurer
PRICE_ALERT_THRESHOLD = 0.0030804  # Modifier ce niveau de prix selon vos besoins

# Fonction pour envoyer un email d'alerte
def send_email_alert(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email envoyé avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Fonction pour récupérer les données historiques de prix
def get_historical_data():
    response = requests.get(POOL_URL)
    data = response.json()
    prices = data['data']['attributes']['chart']['points']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    return df

# Fonction pour calculer le MACD
def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA_12'] = df['price'].ewm(span=short_window, adjust=False).mean()
    df['EMA_26'] = df['price'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df

# Fonction pour détecter le croisement des lignes MACD
def detect_macd_cross(df):
    if len(df) < 2:
        return False
    latest_macd = df['MACD'].iloc[-1]
    latest_signal = df['Signal_Line'].iloc[-1]
    previous_macd = df['MACD'].iloc[-2]
    previous_signal = df['Signal_Line'].iloc[-2]

    # Vérifie si les lignes convergent et se croisent
    if previous_macd < previous_signal and latest_macd > latest_signal:
        return True
    return False

# Fonction pour détecter le seuil de prix
def detect_price_alert(df):
    latest_price = df['price'].iloc[-1]
    if latest_price >= PRICE_ALERT_THRESHOLD:
        return True, latest_price
    return False, latest_price

# Fonction principale
if __name__ == "__main__":
    print("Démarrage du script de surveillance MACD et alerte de prix...")
    while True:
        try:
            df = get_historical_data()
            df = calculate_macd(df)

            # Vérification du croisement MACD
            if detect_macd_cross(df):
                print(f"\n[ALERTE] Croisement MACD détecté à {datetime.now()} !")
                subject = "ALERTE MACD - Croisement détecté"
                body = f"Un croisement MACD a été détecté sur le token suivi à {datetime.now()}"
                send_email_alert(subject, body)

            # Vérification du seuil de prix
            price_alert, latest_price = detect_price_alert(df)
            if price_alert:
                print(f"\n[ALERTE] Seuil de prix atteint : {latest_price} SOL à {datetime.now()} !")
                subject = "ALERTE PRIX - Seuil atteint"
                body = f"Le seuil de prix de {PRICE_ALERT_THRESHOLD} SOL a été atteint. Dernier prix : {latest_price} SOL."
                send_email_alert(subject, body)

            else:
                print(f"{datetime.now()} - Aucun croisement MACD détecté. Prix actuel : {latest_price} SOL")

            sleep(3600)  # Vérifie toutes les heures
        except Exception as e:
            print(f"Erreur : {e}")
            sleep(60)  # Attente en cas d'erreur
