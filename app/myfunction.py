import numpy as np
import pickle as pk
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
        with open(in_model, 'rb') as md:
            load_model = pk.load(md)
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
