import streamlit as st
import matplotlib.pyplot as plt
import math

st.title("📊 Aplikasi Model Matematika Industri")

# ===== Sidebar: Dokumentasi =====
st.sidebar.markdown("## 📘 Instruksi Penggunaan")
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
    ["Optimisasi Produksi (LP)", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Model Industri Lainnya"]
)

# ===== Konten Utama berdasarkan menu =====

# --- Model 1: Linear Programming (Placeholder)
if menu == "Optimisasi Produksi (LP)":
    st.header("🔧 Optimisasi Produksi (Linear Programming)")
    st.write("Masukkan data untuk menyelesaikan persoalan LP...")

# --- Model 2: EOQ
elif menu == "Model Persediaan (EOQ)":
    st.header("📦 Model Persediaan EOQ")
    
    # Input
    D = st.number_input("Permintaan per Tahun (D)", value=1000)
    S = st.number_input("Biaya Pemesanan (S)", value=50)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=10)

    # EOQ formula
    EOQ = math.sqrt((2 * D * S) / H)
    st.success(f"📌 EOQ: {EOQ:.2f} unit")

    # Grafik EOQ
    Q = list(range(100, 2000, 100))
    TC = [((D / q) * S + (q / 2) * H) for q in Q]  # Total Cost
    fig, ax = plt.subplots()
    ax.plot(Q, TC, label='Total Cost')
    ax.axvline(EOQ, color='r', linestyle='--', label='EOQ')
    ax.set_xlabel('Order Quantity')
    ax.set_ylabel('Total Cost')
    ax.set_title('EOQ vs Total Cost')
    ax.legend()
    st.pyplot(fig)

# --- Model 3: Antrian M/M/1
elif menu == "Model Antrian (M/M/1)":
    st.header("⏳ Model Antrian M/M/1")
    
    lam = st.number_input("Tingkat Kedatangan (λ)", value=6.0)
    mu = st.number_input("Tingkat Pelayanan (μ)", value=8.0)
    
    if lam >= mu:
        st.error("λ harus lebih kecil dari μ agar sistem stabil.")
    else:
        rho = lam / mu
        L = rho / (1 - rho)
        W = 1 / (mu - lam)
        st.write(f"Utilisasi Sistem (ρ): {rho:.2f}")
        st.write(f"Rata-rata pelanggan dalam sistem (L): {L:.2f}")
        st.write(f"Waktu tunggu rata-rata (W): {W:.2f}")

        # Grafik: Utilisasi (ρ) terhadap W
        lam_range = [x for x in range(1, int(mu))]
        w_values = [1 / (mu - l) for l in lam_range]
        fig, ax = plt.subplots()
        ax.plot(lam_range, w_values, label="Waktu Tunggu (W)")
        ax.set_xlabel("Tingkat Kedatangan (λ)")
        ax.set_ylabel("Waktu Tunggu")
        ax.set_title("Pengaruh λ terhadap Waktu Tunggu")
        st.pyplot(fig)

# --- Model 4: Breakeven Point
elif menu == "Model Industri Lainnya":
    st.header("🏭 Model Industri Lainnya (Break Even Point)")
    
    FC = st.number_input("Biaya Tetap (FC)", value=1000)
    VC = st.number_input("Biaya Variabel per Unit (VC)", value=20)
    P = st.number_input("Harga Jual per Unit (P)", value=50)

    if P > VC:
        BEQ = FC / (P - VC)
        st.success(f"📌 Break Even Quantity: {BEQ:.0f} unit")

        # Grafik BEP
        Q = list(range(0, int(BEQ) * 2, 10))
        TR = [P * q for q in Q]
        TC = [FC + VC * q for q in Q]

        fig, ax = plt.subplots()
        ax.plot(Q, TR, label="Total Revenue (TR)")
        ax.plot(Q, TC, label="Total Cost (TC)")
        ax.axvline(BEQ, color='r', linestyle='--', label='BEP')
        ax.set_xlabel('Jumlah Unit')
        ax.set_ylabel('Rp')
        ax.set_title('Break Even Point')
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("⚠ Harga Jual harus lebih besar dari Biaya Variabel!")

# ===== Footer =====
st.markdown("---")
st.markdown("📌 Dibuat oleh Kelompok [kelompok 4] - 2025")
