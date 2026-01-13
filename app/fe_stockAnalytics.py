import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
from app import myfunction as mf

stockAnalytics = mf.allFunction.calc_levels_with_fair_value

def compute_macd(df, short_window=12, long_window=26, signal_window=9):
    df = df.sort_index()
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal_Line']
    return df

def app():
    st.title("📊 MACD Visualization for Stock Analysis")
    st.markdown("""In this study, we develop a **stock analysis model** that utilizes the **Support and Resistance approach**...""")
    
    default_tickers = ["BBRI.JK", "BBCA.JK"]
    tickers = st.multiselect("Select Stock Tickers:", 
                             ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK", "TLKM.JK", "ANTM.JK", "ASII.JK", "GOTO.JK"],
                             default=default_tickers)

    today = datetime.date.today()
    start_of_year = datetime.date(today.year, 1, 1)
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=start_of_year)
    with col2:
        end_date = st.date_input("End Date", value=today)      

    if st.button("🔍 Show MACD Chart"):
        if not tickers:
            st.warning("Please select at least one ticker.")
            return

        st.info(f"Fetching data for {', '.join(tickers)}...")
        
        try:
            # Download data
            data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', threads=True)
            
            if data.empty:
                st.error("No data found. Please check your internet connection or ticker symbols.")
                return

            results_dict = {}
            valid_tickers = [] # List untuk menyimpan ticker yang datanya valid

            # --- PROSES ANALISIS (Support, Resistance, Fair Value) ---
            for t in tickers:
                # Logika ekstraksi data (Handle Single vs Multi Ticker structure)
                try:
                    if len(tickers) > 1:
                        df_t = data[t]
                    else:
                        # Jika hanya 1 ticker, yfinance kadang tidak pakai MultiIndex
                        df_t = data if isinstance(data.columns, pd.MultiIndex) else data
                    
                    # Cek apakah DataFrame kosong
                    if df_t is None or df_t.empty:
                        continue

                    # Jalankan fungsi custom (stockAnalytics)
                    res = stockAnalytics(df_t)
                    
                    if res is not None:
                        results_dict[t] = res
                        valid_tickers.append(t) # Masukkan ke list valid

                except KeyError:
                    st.warning(f"Data struct error for {t}. Skipping.")
                    continue

            # --- MENAMPILKAN TABEL HASIL ---
            results = pd.DataFrame(results_dict).T
            
            st.success("✅ Analysis Complete")
            st.subheader("📋 Support, Resistance & Fair Value Summary")

            if not results.empty:
                # Filter kolom agar tidak error jika kolom tidak ditemukan
                target_cols = ['Pivot', 'S1', 'R1', 'Fair_Buy', 'Fair_Sell', 'Trend_Signal']
                valid_cols = [col for col in target_cols if col in results.columns]
                
                if valid_cols:
                    st.dataframe(results[valid_cols])
                else:
                    st.dataframe(results) # Tampilkan semua jika kolom target tidak ada
            else:
                st.warning("Could not calculate Support/Resistance levels for the selected stocks.")

            # --- MENAMPILKAN GRAFIK MACD ---
            for t in valid_tickers:
                st.markdown("---") # Garis pemisah
                st.subheader(f"📈 {t} — MACD Indicator")
                
                # Ambil data lagi untuk plotting
                if len(tickers) > 1:
                    df = data[t].copy()
                else:
                    df = data.copy()

                # Hitung MACD
                df = compute_macd(df)
                
                # Drop NaN awal akibat perhitungan EMA
                df = df.dropna(subset=['MACD', 'Signal_Line'])

                if df.empty:
                    st.write(f"Not enough data to plot MACD for {t}")
                    continue

                # Plotting
                fig, ax = plt.subplots(figsize=(10, 4))
                
                # Plot Lines
                ax.plot(df.index, df['MACD'], label='MACD', color='blue', linewidth=1.5)
                ax.plot(df.index, df['Signal_Line'], label='Signal Line', color='red', linewidth=1.2)
                
                # Plot Histogram dengan warna
                # Handle error jika MACD_Hist berisi NaN
                hist_colors = ['green' if (v >= 0) else 'red' for v in df['MACD_Hist'].fillna(0)]
                ax.bar(df.index, df['MACD_Hist'], color=hist_colors, alpha=0.4, label='Histogram')
                
                ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
                ax.legend(loc="upper left", fontsize=8)
                ax.set_title(f"{t} — MACD Momentum", fontsize=12)
                ax.set_ylabel("Value")
                ax.grid(alpha=0.3)
                
                # Render ke Streamlit
                st.pyplot(fig)
                plt.close(fig) # Penting untuk hemat memori

                # Sinyal Terakhir
                latest_macd = df['MACD'].iloc[-1]
                latest_signal = df['Signal_Line'].iloc[-1]
                
                col_sig1, col_sig2 = st.columns([1, 4])
                with col_sig1:
                    st.metric("MACD Value", f"{latest_macd:.2f}")
                with col_sig2:
                    if latest_macd > latest_signal:
                        st.success(f"💹 **Bullish Signal for {t}:** MACD is above Signal Line.")
                    elif latest_macd < latest_signal:
                        st.error(f"🔻 **Bearish Signal for {t}:** MACD is below Signal Line.")
                    else:
                        st.info("⚖️ **Neutral:** No clear crossover.")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Jalankan aplikasi
if __name__ == "__main__":
    app()



# import streamlit as st
# import pandas as pd
# import yfinance as yf
# import matplotlib.pyplot as plt
# from app import myfunction as mf

# stockAnalytics = mf.allFunction.calc_levels_with_fair_value

# def compute_macd(df, short_window=12, long_window=26, signal_window=9):
#     df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
#     df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
#     df['MACD'] = df['EMA12'] - df['EMA26']
#     df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
#     df['MACD_Hist'] = df['MACD'] - df['Signal_Line']
#     return df

# def app():
#     st.title("📊 MACD Visualization for Stock Analysis")
#     st.markdown("""In this study, we develop a **stock analysis model** that utilizes the **Support and Resistance approach** to identify
#     potential entry and exit zones while confirming price movement strength through **volume analysis**. The methodology,
#     code implementation, and data processing details — including **historical price retrieval, pivot-based level computation (S1–R2),
#     Volume confirmation**, and **fair value estimation** for buy/sell decisions — are explained in my publication
#     *“Stock Analysis Using Support and Resistance”* (available on Google Scholar).""")
    
#     tickers = st.multiselect("Select Stock Tickers:", ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK", "TLKM.JK", "ANTM.JK"],
#                              default=["BBRI.JK", "BBCA.JK"])

#     start_date = st.date_input("Start Date", value=pd.to_datetime("2025-01-01"))
#     end_date = st.date_input("End Date", value=pd.to_datetime("2025-10-07"))        

#     if st.button("🔍 Show MACD Chart"):
#         st.info("Fetching data and calculating MACD...")
#         data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
#         results_dict = {}
#         for t in tickers:
#         # Pastikan data[t] tidak kosong sebelum diproses
#             if not data[t].empty:
#                 res = stockAnalytics(data[t])
#                 if res is not None: # Pastikan hasil fungsi tidak None
#                     results_dict[t] = res
#         results = pd.DataFrame(results_dict).T
#         # results = pd.DataFrame({t: stockAnalytics(data[t]) for t in tickers}).T
#         st.success("✅ Analysis Complete")
#         st.subheader("📋 Support, Resistance & Fair Value Summary")
#         st.dataframe(results[['Pivot', 'S1', 'R1', 'Fair_Buy', 'Fair_Sell', 'Trend_Signal']])

#         for t in tickers:
#             st.subheader(f"📈 {t} — MACD Indicator")
#             df = data[t].copy()
#             df = compute_macd(df)
#             fig, ax = plt.subplots(figsize=(10, 4))
#             ax.plot(df.index, df['MACD'], label='MACD', color='blue', linewidth=1.5)
#             ax.plot(df.index, df['Signal_Line'], label='Signal Line', color='red', linewidth=1.2)
#             ax.bar(df.index, df['MACD_Hist'],
#                    color=['green' if v >= 0 else 'red' for v in df['MACD_Hist']],
#                    alpha=0.4, label='Histogram')
#             ax.axhline(0, color='gray', linewidth=0.8)
#             ax.legend(loc="upper left", fontsize=8)
#             ax.set_title(f"{t} — MACD Momentum Indicator", fontsize=12)
#             ax.grid(alpha=0.3)
#             st.pyplot(fig)

#             latest_macd = df['MACD'].iloc[-1]
#             latest_signal = df['Signal_Line'].iloc[-1]
#             if latest_macd > latest_signal:
#                 st.markdown("💹 **Buy Signal:** MACD crosses above the signal line (bullish momentum).")
#             elif latest_macd < latest_signal:
#                 st.markdown("🔻 **Sell Signal:** MACD crosses below the signal line (bearish momentum).")
#             else:
#                 st.markdown("⚖️ **Neutral:** No clear crossover detected.")

# # Jalankan aplikasi
# if __name__ == "__main__":
#     app()
