import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score

# --- KONFIGURASI KELAS & DISTRIBUSI SINTETIS ---
CLASS_NAMES = [
    'Business Flash Visit', 'Leisure Planner', 'Last-Minute Bargain Hunter',
    'Premium Spontaneous', 'Extended-Stay Value Seeker', 'Loyal Repeat Guest'
]

# [LOS_mean, LOS_sd, BW_mean, BW_sd, ADR_mean, ADR_sd]
SYNTH_CENTERS = [
    [1.5, 0.5, 1.5, 1.0, 1100, 180],
    [5.5, 1.5, 55, 18, 750, 150],
    [2.0, 0.8, 1.0, 0.7, 480, 90],
    [1.8, 0.7, 3.0, 2.0, 1900, 250],
    [10.0, 2.5, 20, 7, 600, 110],
    [3.8, 1.0, 17, 6, 950, 140],
]


# Fungsi untuk generate data sintetis
def generate_samples(class_idx, count=8):
    lm, lsd, bm, bsd, am, asd = SYNTH_CENTERS[class_idx]
    new_samples = []
    for _ in range(count):
        los = max(1, round(np.random.normal(lm, lsd)))
        bw = max(0, round(np.random.normal(bm, bsd)))
        adr = max(50, round(np.random.normal(am, asd)))
        new_samples.append([los, bw, adr])
    st.session_state.samples[CLASS_NAMES[class_idx]].extend(new_samples)


def app():
    if 'samples' not in st.session_state:
        st.session_state.samples = {name: [] for name in CLASS_NAMES}
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'accuracy' not in st.session_state:
        st.session_state.accuracy = None

    # --- HEADER ---
    st.title("Guest Archetype Classifier")
    st.markdown("Latih klasifikasi tipe tamu langsung dari fitur LOS, Booking Window, dan ADR.")

    # --- LAYOUT 3 KOLOM ---
    col1, col2, col3 = st.columns(3)

    # ===================== PANEL 1: KUMPULKAN DATA =====================
    with col1:
        st.header("1. Kumpulkan Data")
        st.caption("Enam arketipe tamu dengan fitur numerik.")

        if st.button("🎲 Generate contoh data untuk semua kelas", use_container_width=True):
            for i in range(len(CLASS_NAMES)):
                generate_samples(i, 10)
            st.rerun()

        if st.button("Hapus semua sampel", use_container_width=True):
            st.session_state.samples = {name: [] for name in CLASS_NAMES}
            st.session_state.model = None
            st.session_state.accuracy = None
            st.rerun()

        for i, cls_name in enumerate(CLASS_NAMES):
            with st.expander(f"{cls_name} ({len(st.session_state.samples[cls_name])} sampel)"):
                if st.button("🎲 +8 sintetis", key=f"gen_{i}"):
                    generate_samples(i, 8)
                    st.rerun()

                df = pd.DataFrame(st.session_state.samples[cls_name], columns=["LOS", "BW", "ADR"])
                if not df.empty:
                    st.dataframe(df, height=150)

    # ===================== PANEL 2: LATIH MODEL =====================
    with col2:
        st.header("2. Latih Model")
        st.caption("Minimal 3 sampel per kelas. Akurasi dihitung lewat LOO-CV.")

        total_samples = sum(len(s) for s in st.session_state.samples.values())
        ready_classes = sum(1 for s in st.session_state.samples.values() if len(s) >= 3)

        st.metric("Total Sampel", total_samples)
        st.metric("Kelas Siap", f"{ready_classes} / 6")

        acc_text = f"{(st.session_state.accuracy * 100):.1f}%" if st.session_state.accuracy is not None else "–"
        st.metric("Akurasi (LOO-CV)", acc_text)

        can_train = ready_classes == 6

        if st.button("▶ Latih Model", disabled=not can_train, type="primary", use_container_width=True):
            X, y = [], []
            for cls_name, samples in st.session_state.samples.items():
                for sample in samples:
                    X.append(sample)
                    y.append(cls_name)

            X = np.array(X)
            y = np.array(y)

            # Cross-validation (LOO-CV)
            loo = LeaveOneOut()
            y_pred = []
            model_cv = GaussianNB()
            for train_index, test_index in loo.split(X):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                model_cv.fit(X_train, y_train)
                y_pred.append(model_cv.predict(X_test)[0])

            st.session_state.accuracy = accuracy_score(y, y_pred)

            # Final Model fit on all data
            final_model = GaussianNB()
            final_model.fit(X, y)
            st.session_state.model = final_model
            st.rerun()

    # ===================== PANEL 3: UJI & EKSPOR =====================
    with col3:
        st.header("3. Uji & Ekspor")
        st.caption("Geser nilai fitur tamu baru dan lihat distribusi keyakinan model.")

        if st.session_state.model is None:
            st.info("Latih model dulu di Panel 2 untuk mengaktifkan pengujian.")
        else:
            los_val = st.slider("Length of Stay (malam)", min_value=1, max_value=16, value=3, step=1)
            bw_val = st.slider("Booking Window (hari)", min_value=0, max_value=100, value=14, step=1)
            adr_val = st.slider("ADR (ribu / malam)", min_value=200, max_value=2500, value=800, step=10)

            # Prediksi
            input_features = np.array([[los_val, bw_val, adr_val]])
            probs = st.session_state.model.predict_proba(input_features)[0]
            classes_order = st.session_state.model.classes_

            # Format probabilitas untuk ditampilkan
            prob_df = pd.DataFrame({
                'Arketipe': classes_order,
                'Keyakinan (%)': np.round(probs * 100, 1)
            }).sort_values(by='Keyakinan (%)', ascending=False)

            st.write("**Hasil Prediksi:**")
            st.dataframe(prob_df, hide_index=True, use_container_width=True)

            # Logika Ekspor JSON
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "feature_order": ['length_of_stay', 'booking_window', 'adr'],
                "classes": []
            }

            for i, cls_name in enumerate(st.session_state.model.classes_):
                export_data["classes"].append({
                    "name": cls_name,
                    "n_samples": int(np.sum(st.session_state.model.class_count_[i])),
                    "mean": st.session_state.model.theta_[i].tolist(),
                    "std": np.sqrt(st.session_state.model.var_[i]).tolist()
                })

            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="⬇ Ekspor model (.json)",
                file_name="guest-archetype-model.json",
                mime="application/json",
                data=json_str,
                use_container_width=True
            )
