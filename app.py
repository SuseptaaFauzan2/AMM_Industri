import streamlit as st
import matplotlib.pyplot as plt
import math
from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, LpStatus, value

st.set_page_config(page_title="Model Matematika Industri", layout="wide")
st.title("\U0001F4CA Aplikasi Model Matematika Industri")

# ===== Sidebar: Dokumentasi =====
st.sidebar.markdown("## \U0001F4D8 Instruksi Penggunaan")
st.sidebar.write("""
Selamat datang di aplikasi model matematika industri.

🛠 Cara menggunakan:
1. Pilih salah satu model di menu dropdown.
2. Masukkan parameter yang diminta.
3. Lihat hasil perhitungan dan grafik visualisasi.
""")

# ===== Sidebar: Pilih Model =====
menu = st.sidebar.selectbox(
    "Pilih Model:",
    ["Optimisasi Produksi (LP)", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Break Even Point (BEP)"]
)

# ===== Model 1: Linear Programming =====
if menu == "Optimisasi Produksi (LP)":
    st.header("\U0001F527 Optimisasi Produksi (Linear Programming)")
    st.subheader("\U0001F4D6 Studi Kasus: Produksi Makanan Kaleng")

    profit_A = st.number_input("Laba per Unit Produk A", value=30.0)
    resource1_A = st.number_input("Mesin per Unit Produk A", value=2.0)
    resource2_A = st.number_input("Tenaga Kerja per Unit Produk A", value=1.0)
    profit_B = st.number_input("Laba per Unit Produk B", value=50.0)
    resource1_B = st.number_input("Mesin per Unit Produk B", value=3.0)
    resource2_B = st.number_input("Tenaga Kerja per Unit Produk B", value=4.0)
    limit_resource1 = st.number_input("Kapasitas Mesin", value=100.0)
    limit_resource2 = st.number_input("Kapasitas Tenaga Kerja", value=120.0)

    if st.button("Hitung Optimasi"):
        prob = LpProblem("Optimalisasi_Produksi", LpMaximize)
        x_A = LpVariable("Jumlah_Produk_A", 0, None, LpInteger)
        x_B = LpVariable("Jumlah_Produk_B", 0, None, LpInteger)
        prob += profit_A * x_A + profit_B * x_B
        prob += resource1_A * x_A + resource1_B * x_B <= limit_resource1
        prob += resource2_A * x_A + resource2_B * x_B <= limit_resource2
        prob.solve()

        st.subheader("Hasil Optimasi:")
        if LpStatus[prob.status] == "Optimal":
            st.success(f"Laba Maksimal: Rp {value(prob.objective):,.2f}")
            st.write(f"Jumlah Produk A: {x_A.varValue:.0f} unit")
            st.write(f"Jumlah Produk B: {x_B.varValue:.0f} unit")

            fig, ax = plt.subplots()
            x_vals = [0, limit_resource1 / resource1_A]
            y_vals1 = [(limit_resource1 - resource1_A * x) / resource1_B for x in x_vals]
            ax.plot(x_vals, y_vals1, label='Kapasitas Mesin', linestyle='--')

            x_vals = [0, limit_resource2 / resource2_A]
            y_vals2 = [(limit_resource2 - resource2_A * x) / resource2_B for x in x_vals]
            ax.plot(x_vals, y_vals2, label='Kapasitas Tenaga Kerja', linestyle='--')

            ax.plot(x_A.varValue, x_B.varValue, 'ro', label='Titik Optimal')
            ax.set_xlabel("Produk A")
            ax.set_ylabel("Produk B")
            ax.set_title("Area Feasible dan Titik Optimal")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)
        else:
            st.error("Tidak ada solusi optimal.")

# ===== Model 2: EOQ =====
elif menu == "Model Persediaan (EOQ)":
    st.header("\U0001F4E6 Model Persediaan EOQ")
    st.subheader("\U0001F4D6 Studi Kasus: Pengadaan Bahan Baku Pabrik")

    D = st.number_input("Permintaan Tahunan (D)", value=1200.0)
    S = st.number_input("Biaya Pemesanan per Order (S)", value=50000.0)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2000.0)

    if H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit per order")

        Q_range = list(range(1, int(EOQ*2), max(1, int(EOQ*0.1))))
        total_cost = [(D/q)*S + (q/2)*H for q in Q_range]

        fig, ax = plt.subplots()
        ax.plot(Q_range, total_cost, label="Total Cost")
        ax.axvline(EOQ, color='r', linestyle='--', label="EOQ")
        ax.set_xlabel("Order Quantity")
        ax.set_ylabel("Total Cost")
        ax.set_title("Grafik EOQ vs Biaya Total")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
    else:
        st.error("Biaya penyimpanan harus lebih dari 0.")

# ===== Model 3: Antrian M/M/1 =====
elif menu == "Model Antrian (M/M/1)":
    st.header("\u23F3 Model Antrian M/M/1")
    st.subheader("\U0001F4D6 Studi Kasus: Antrian Pemeriksaan Kualitas Produk")

    lam = st.number_input("Laju Kedatangan Produk (λ)", value=4.0)
    mu = st.number_input("Laju Pemeriksaan (μ)", value=6.0)

    if lam >= mu:
        st.error("Sistem tidak stabil: λ harus < μ")
    else:
        rho = lam / mu
        W = 1 / (mu - lam)
        st.write(f"Utilisasi Sistem (ρ): {rho:.2f}")
        st.write(f"Waktu Tunggu Rata-rata: {W:.2f} jam")

        lam_vals = [x * 0.1 for x in range(1, int(mu * 10)) if x * 0.1 < mu]
        W_vals = [1 / (mu - l) for l in lam_vals]

        fig, ax = plt.subplots()
        ax.plot(lam_vals, W_vals, label="Waktu Tunggu (W)")
        ax.set_xlabel("Laju Kedatangan (λ)")
        ax.set_ylabel("Waktu Tunggu (W)")
        ax.set_title("Pengaruh λ terhadap W")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

# ===== Model 4: Break Even Point =====
elif menu == "Break Even Point (BEP)":
    st.header("\U0001F3ED Break Even Point (BEP)")
    st.subheader("\U0001F4D6 Studi Kasus: Produksi Minuman Botol")

    FC = st.number_input("Biaya Tetap (FC)", value=10000000.0)
    VC = st.number_input("Biaya Variabel per Unit (VC)", value=8000.0)
    P = st.number_input("Harga Jual per Unit (P)", value=12000.0)

    if P > VC:
        BEQ = FC / (P - VC)
        st.success(f"Break Even Quantity (BEP): {BEQ:.0f} unit")

        Q = list(range(0, int(BEQ*2), max(1, int(BEQ*0.1))))
        TR = [P * q for q in Q]
        TC = [FC + VC * q for q in Q]

        fig, ax = plt.subplots()
        ax.plot(Q, TR, label="Total Revenue")
        ax.plot(Q, TC, label="Total Cost")
        ax.axvline(BEQ, color='r', linestyle='--', label="BEP")
        ax.set_xlabel("Jumlah Unit")
        ax.set_ylabel("Rp")
        ax.set_title("Break Even Point")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
    else:
        st.error("Harga jual harus lebih besar dari biaya variabel.")

# ===== Footer =====
st.markdown("---")
st.markdown("\U0001F4CC Dibuat oleh Kelompok 4 - 2025")
