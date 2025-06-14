import streamlit as st
import matplotlib.pyplot as plt
import math
from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, LpStatus, value

st.title("📊 Aplikasi Model Matematika Industri")

# ===== Sidebar: Dokumentasi =====
st.sidebar.markdown("## 📘 Instruksi Penggunaan")
st.sidebar.write("""
Selamat datang di aplikasi model matematika industri.

🛠️ Cara menggunakan:
1. Pilih salah satu model di menu dropdown.
2. Masukkan parameter yang diminta.
3. Lihat hasil perhitungan dan grafik visualisasi.
""")

# ===== Sidebar: Pilih Model =====
menu = st.sidebar.selectbox(
    "Pilih Model:",
    ["Optimisasi Produksi (LP)", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Break Even Point (BEP)"]
)

# ===== Konten Utama berdasarkan menu =====

# --- Model 1: Linear Programming (Optimisasi Produksi)
if menu == "Optimisasi Produksi (LP)":
    st.header("🔧 Optimisasi Produksi (Linear Programming)")
    st.subheader("📖 Studi Kasus: Produksi Makanan Kaleng")
    st.write("""
Sebuah pabrik makanan ingin memproduksi dua jenis produk: **Produk A (sarden)** dan **Produk B (kornet)**. 
Masing-masing produk memberikan laba berbeda dan memerlukan dua jenis sumber daya utama: mesin dan tenaga kerja.
Manajemen ingin mengetahui berapa banyak produk yang harus dibuat untuk **memaksimalkan laba**, 
dengan tetap mematuhi batas ketersediaan sumber daya yang ada.
""")

    st.markdown("---")
    st.subheader("Parameter Input:")
    
    st.write("### Produk A")
    profit_A = st.number_input("Laba per Unit Produk A", value=30.0, key="profit_A")
    resource1_A = st.number_input("Kebutuhan Sumber Daya 1 per Unit Produk A", value=2.0, key="res1_A")
    resource2_A = st.number_input("Kebutuhan Sumber Daya 2 per Unit Produk A", value=1.0, key="res2_A")

    st.write("### Produk B")
    profit_B = st.number_input("Laba per Unit Produk B", value=50.0, key="profit_B")
    resource1_B = st.number_input("Kebutuhan Sumber Daya 1 per Unit Produk B", value=3.0, key="res1_B")
    resource2_B = st.number_input("Kebutuhan Sumber Daya 2 per Unit Produk B", value=4.0, key="res2_B")

    st.write("### Batasan Sumber Daya")
    limit_resource1 = st.number_input("Ketersediaan Maksimal Sumber Daya 1", value=100.0, key="limit_res1")
    limit_resource2 = st.number_input("Ketersediaan Maksimal Sumber Daya 2", value=120.0, key="limit_res2")

    if st.button("Hitung Optimasi"):
        prob = LpProblem("Optimalisasi_Produksi", LpMaximize)
        x_A = LpVariable("Jumlah_Produk_A", 0, None, LpInteger)
        x_B = LpVariable("Jumlah_Produk_B", 0, None, LpInteger)

        prob += profit_A * x_A + profit_B * x_B, "Total Laba"
        prob += resource1_A * x_A + resource1_B * x_B <= limit_resource1
        prob += resource2_A * x_A + resource2_B * x_B <= limit_resource2

        prob.solve()

        st.subheader("Hasil Optimasi:")
        if LpStatus[prob.status] == "Optimal":
            st.success(f"Status: **{LpStatus[prob.status]}**")
            st.write(f"Produk A yang optimal diproduksi: **{x_A.varValue:.0f} unit**")
            st.write(f"Produk B yang optimal diproduksi: **{x_B.varValue:.0f} unit**")
            st.write(f"**Laba Maksimal:** Rp **{value(prob.objective):.2f}**")

            st.markdown("---")
            st.subheader("Visualisasi (Area Feasible - Sederhana):")
            fig, ax = plt.subplots()
            if resource1_B != 0:
                x_A_vals = [0, limit_resource1 / resource1_A if resource1_A != 0 else 0]
                x_B_vals_res1 = [(limit_resource1 - resource1_A * x) / resource1_B for x in x_A_vals]
                ax.plot(x_A_vals, x_B_vals_res1, label=f'Sumber Daya 1 <= {limit_resource1}', linestyle='--')

            if resource2_B != 0:
                x_A_vals = [0, limit_resource2 / resource2_A if resource2_A != 0 else 0]
                x_B_vals_res2 = [(limit_resource2 - resource2_A * x) / resource2_B for x in x_A_vals]
                ax.plot(x_A_vals, x_B_vals_res2, label=f'Sumber Daya 2 <= {limit_resource2}', linestyle='--')

            ax.plot(x_A.varValue, x_B.varValue, 'ro', markersize=8, label='Titik Optimal')
            ax.text(x_A.varValue + 2, x_B.varValue + 2, f'({x_A.varValue:.0f}, {x_B.varValue:.0f})', fontsize=10)
            ax.set_xlabel('Jumlah Produk A')
            ax.set_ylabel('Jumlah Produk B')
            ax.set_title('Area Feasible dan Titik Optimal (Sederhana)')
            ax.set_xlim(0)
            ax.set_ylim(0)
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.error(f"Status: **{LpStatus[prob.status]}**. Tidak ada solusi optimal ditemukan.")

# --- Model 2: EOQ
elif menu == "Model Persediaan (EOQ)":
    st.header("📦 Model Persediaan EOQ")
    st.subheader("📖 Studi Kasus: Pengadaan Komponen Elektronik")
    st.write("""
Sebuah perusahaan manufaktur memproduksi alat elektronik dan secara rutin memesan komponen resistor dari pemasok. 
Permintaan diperkirakan konstan setiap tahun. Setiap kali memesan dikenakan biaya tetap, dan setiap unit yang disimpan memiliki biaya penyimpanan tahunan.
Perusahaan ingin mengetahui **jumlah pemesanan optimal** untuk meminimalkan total biaya persediaan.
""")

    D = st.number_input("Permintaan per Tahun (D)", value=1000.0)
    S = st.number_input("Biaya Pemesanan (S)", value=50.0)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=10.0)

    if H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"📌 EOQ: {EOQ:.2f} unit")
    else:
        st.error("Biaya Penyimpanan (H) harus lebih besar dari 0.")

# --- Model 3: Antrian M/M/1
elif menu == "Model Antrian (M/M/1)":
    st.header("⏳ Model Antrian M/M/1")
    st.subheader("📖 Studi Kasus: Pelayanan di Loket Bank")
    st.write("""
Sebuah bank memiliki satu loket pelayanan pelanggan. Rata-rata terdapat 6 pelanggan datang per jam, 
dan satu petugas mampu melayani rata-rata 8 pelanggan per jam. 
Manajemen ingin mengetahui performa sistem antrian seperti **berapa rata-rata waktu tunggu** dan **jumlah pelanggan yang menumpuk**.
""")

    lam = st.number_input("Tingkat Kedatangan (λ)", value=6.0)
    mu = st.number_input("Tingkat Pelayanan (μ)", value=8.0)

    if lam >= mu:
        st.error("λ harus lebih kecil dari μ agar sistem stabil.")
    else:
        rho = lam / mu
        L = rho / (1 - rho)
        W = 1 / (mu - lam)
        Lq = L - rho
        Wq = W - (1/mu)

        st.write(f"Utilisasi Sistem (ρ): {rho:.2f}")
        st.write(f"Rata-rata pelanggan dalam sistem (L): {L:.2f} pelanggan")
        st.write(f"Waktu tunggu rata-rata dalam sistem (W): {W:.2f} unit waktu")
        st.write(f"Rata-rata pelanggan dalam antrian (Lq): {Lq:.2f} pelanggan")
        st.write(f"Waktu tunggu rata-rata dalam antrian (Wq): {Wq:.2f} unit waktu")

# --- Model 4: Break Even Point
elif menu == "Break Even Point (BEP)":
    st.header("🏭 Break Even Point (BEP)")
    st.subheader("📖 Studi Kasus: Usaha Minuman Botol")
    st.write("""
Seorang pengusaha memproduksi minuman botol dengan biaya tetap produksi seperti sewa alat dan gaji karyawan tetap. 
Setiap botol memiliki biaya variabel dan dijual dengan harga tertentu.
Pengusaha ingin tahu **berapa banyak botol yang harus dijual untuk balik modal (Break Even Point)**.
""")

    FC = st.number_input("Biaya Tetap (FC)", value=1000.0)
    VC = st.number_input("Biaya Variabel per Unit (VC)", value=20.0)
    P = st.number_input("Harga Jual per Unit (P)", value=50.0)

    if P > VC:
        BEQ = FC / (P - VC)
        st.success(f"📌 Break Even Quantity: {BEQ:.0f} unit")
    else:
        st.error("⚠️ Harga Jual harus lebih besar dari Biaya Variabel!")

# ===== Footer =====
st.markdown("---")
st.markdown("📌 Dibuat oleh Kelompok 4 - 2025")
