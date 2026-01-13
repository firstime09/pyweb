import numpy as np
import pandas as pd
import pickle, gzip
import streamlit as st
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

class allFunction:
    def sigmoid_func(x):
        hit = 1/(1 + np.exp(x))
        return hit
    
    def load_model(in_model):
        with gzip.open(in_model, 'rb') as md:
            load_model = pickle.load(md)
        return load_model

    def clf_rf_class(dataX, dataY, tsize, rstate):
        X_train, X_test, y_train, y_test = train_test_split(dataX, dataY, test_size=tsize, random_state=rstate)
        sc = MinMaxScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        best_score = 0
        for n_esti in [10, 20, 30, 40, 50, 100]:
            clfRFR = RandomForestClassifier(n_estimators=n_esti, random_state=rstate)
            clfRFR.fit(X_train, y_train)
            score = clfRFR.score(X_test, y_test)
            if score > best_score:
                best_score = score
                total_tree = {'n_estimators': n_esti}
        return(best_score, total_tree, clfRFR)

    def calculate_url_length(url):
        '''Fungsi untuk menghitung total panjang link url'''
        return len(url)
    
    def calculate_www(url):
        hostlen = urlparse(url)
        hostlen = hostlen.hostname
        host_www = 1 if hostlen and 'www' in hostlen.lower() else 0
        return host_www
    
    def calculate_com(url):
        hostlen = urlparse(url)
        hostlen = hostlen.hostname
        host_com = 1 if hostlen and '.com' in hostlen.lower() else 0
        return host_com
    
    def calculate_hostname_length(url):
        '''Fungsi untuk menghitung total panjang link host url'''
        parsed_url = urlparse(url)
        return len(parsed_url.netloc)
    
    def calculate_ratio_digits(string):
        if len(string) == 0:
            return 0
        digit_count = sum(char.isdigit() for char in string)
        return digit_count / len(string)
    
    def output_link(in_model, url1):
        if in_model == 1:
            return(f'{url1}')
        return(f'link is phishing')

    # Fungsi analisis lengkap: Support, Resistance, Volume, dan Harga Wajar ---- 08 Oktober 2025
    def calc_levels_with_fair_value(df):
        high = df['High'].iloc[-1]
        low = df['Low'].iloc[-1]
        close = df['Close'].iloc[-1]
        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        s1 = 2 * pivot - high
        r2 = pivot + (high - low)
        s2 = pivot - (high - low)
        
        # Volume
        avg_vol = df['Volume'][-7:].mean()
        curr_vol = df['Volume'][-1]
        vol_ratio = curr_vol / avg_vol

        # Sinyal tren
        trend_strength = ("Bullish kuat" if (close > pivot and vol_ratio > 1)
                          else "Bearish kuat" if (close < pivot and vol_ratio > 1)
                          else "Netral")

        # Harga wajar beli & jual (dengan bobot tergantung tren)
        alpha = 0.6 if "Bearish" in trend_strength else 0.4
        beta = 0.6 if "Bullish" in trend_strength else 0.4
        fair_buy = pivot - alpha * (pivot - s1)
        fair_sell = pivot + beta * (r1 - pivot)
        
        return pd.Series({'Pivot': pivot, 'R1': r1, 'S1': s1, 'R2': r2, 'S2': s2, 'Avg_Volume': avg_vol, 'Curr_Volume': curr_vol,
                          'Vol_Ratio': vol_ratio, 'Trend_Signal': trend_strength, 'Fair_Buy': fair_buy, 'Fair_Sell': fair_sell})
