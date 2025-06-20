import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# 🌐 Set fullscreen layout
st.set_page_config(page_title="Dashboard Keuangan Juni 2025", layout="wide")

st.title("📅 Dashboard Keuangan Periode Juni 2025")

# ===================== BAGIAN 1: TABEL PENGELUARAN HARIAN =====================
st.header("📋 Tabel Pengeluaran Harian")

# Data pengeluaran harian (default 30 hari)
data_harian = {
    "Date": pd.date_range(start="2025-06-01", end="2025-06-30").strftime("%d/%m/%Y"),
    "Makan": ["" for _ in range(30)],
    "Bensin": ["" for _ in range(30)],
    "Parkir": ["" for _ in range(30)],
    "Ongkos": ["" for _ in range(30)],
    "Shoope": ["" for _ in range(30)],
    "Pulsa": ["" for _ in range(30)],
    "Lain-lain": ["" for _ in range(30)],
}
df_harian = pd.DataFrame(data_harian)

# Sidebar pengaturan
st.sidebar.title("⚙️ Opsi Pengguna")
st.sidebar.markdown("### 👤 Profil")
st.sidebar.markdown("**Nama:** Iqbal")
st.sidebar.markdown("**Periode:** Juni 2025")
st.sidebar.markdown("---")
selected_date = st.sidebar.selectbox("📅 Pilih Tanggal", df_harian["Date"])
st.sidebar.markdown(f"**Tanggal dipilih:** {selected_date}")
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset Tabel"):
    st.experimental_rerun()

if st.sidebar.button("💾 Simpan Pengeluaran Harian"):
    df_harian.to_csv("pengeluaran_harian.csv", index=False)
    st.sidebar.success("✅ Data berhasil disimpan sebagai pengeluaran_harian.csv")

# Konfigurasi AgGrid
gb1 = GridOptionsBuilder.from_dataframe(df_harian)
gb1.configure_default_column(editable=True, resizable=True, filter=True)
gb1.configure_grid_options(rowHeight=35, headerHeight=45, domLayout="normal")

custom_css1 = {
    ".ag-header": {
        "background-color": "#1f4e78",
        "color": "white",
        "font-size": "17px",
        "font-weight": "bold",
        "text-align": "center"
    },
    ".ag-header-cell-label": {
        "justify-content": "center"
    },
    ".ag-cell": {
        "text-align": "center",
        "font-size": "16px",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
        "border": "1px solid #ccc"  # garis antar sel
    },
    ".ag-header-cell": {
        "border": "1px solid #ccc"  # garis antar header
    },
    ".ag-root-wrapper": {
        "border": "1px solid #ccc"  # garis luar
    }
}


grid_response1 = AgGrid(
    df_harian,
    gridOptions=gb1.build(),
    custom_css=custom_css1,
    height=750,
    fit_columns_on_grid_load=True,
    use_container_width=True,
    editable=True
)

edited_df_harian = grid_response1["data"]

# Konversi ke angka
def to_number(val):
    if isinstance(val, str):
        return int(val.replace("Rp", "").replace(",", "").replace(".", "").strip()) if val.strip() else 0
    elif isinstance(val, (int, float)):
        return val
    return 0

# Hitung total per kategori
total_per_kolom = {
    col: sum([to_number(x) for x in edited_df_harian[col]]) for col in edited_df_harian.columns if col != "Date"
}

# Fungsi format rupiah
def format_rp(val):
    return f"Rp{val:,}".replace(",", ".")

# Emoji per kategori
emoji_kategori = {
    "Makan": "🍽️",
    "Bensin": "⛽",
    "Shoope": "📦",
    "Ongkos": "🚌",
    "Parkir": "🅿️",
    "Pulsa": "📱",
    "Lain-lain": "🧾"
}

# Ambil item dalam urutan
kategori_items = list(total_per_kolom.items())

# Judul tengah
st.markdown("<h2 style='text-align: center;'>📊 Total Pengeluaran per Kategori</h2>", unsafe_allow_html=True)

# Formasi 3 - 3 - 1
layout_formasi = [3, 3, 1]
start = 0

for jumlah_kolom in layout_formasi:
    end = start + jumlah_kolom
    baris = kategori_items[start:end]
    cols = st.columns(jumlah_kolom)

    for i, (kategori, total) in enumerate(baris):
        emoji = emoji_kategori.get(kategori, "💼")
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f2f6;
                    padding: 24px;
                    border-radius: 14px;
                    margin: 10px;
                    text-align: center;
                    box-shadow: 1px 1px 6px rgba(0,0,0,0.06);
                ">
                    <div style="font-size: 22px; font-weight: bold;">{emoji} {kategori}</div>
                    <div style="font-size: 22px; margin-top: 10px;">{format_rp(total)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    start = end

st.markdown("<hr>", unsafe_allow_html=True)

# ===================== BAGIAN 2: REKAP PEMASUKAN / PENGELUARAN =====================
st.header("📊 Rekap Keuangan - Periode Juni 2025")

data_rekap = {
    "NO": list(range(1, 11)),
    "Pemasukan": ["KIP-K", "IBU", "BAPAK", "MIRANTI", "AYAH", "BRI", "CASH", "", "", ""],
    "Jumlah Pemasukan": ["", "", "", "", "", "Rp300,000", "Rp3,400,000", "", "", ""],
    "Pengeluaran": ["", "ANDRIAN", "SELVI", "MIRANTI", "AYAH", "SAKIT", "", "", "", ""],
    "Jumlah Pengeluaran": ["", "", "Rp1,000,000", "Rp400,000", "", "", "", "", "", ""],
    "Rincian Biaya": ["Makan", "Shoope", "Bensin", "Parkir", "Ongkos", "Pulsa", "Lain-lain", "", "", ""],
    "Nominal": ["", "", "", "", "", "", "", "", "", ""]
}
df_rekap = pd.DataFrame(data_rekap)

# 👉 Update otomatis kolom "Nominal" berdasarkan total per kategori
df_rekap["Nominal"] = df_rekap["Rincian Biaya"].apply(
    lambda kategori: format_rp(total_per_kolom.get(kategori, 0)) if kategori in total_per_kolom else ""
)

# Lanjut ke AgGrid seperti biasa
gb2 = GridOptionsBuilder.from_dataframe(df_rekap)
gb2.configure_default_column(editable=True, resizable=True, filter=True, cellStyle={"textAlign": "center", "fontSize": "16px"})
gb2.configure_grid_options(domLayout="autoHeight", suppressHorizontalScroll=False)

custom_css2 = {
    ".ag-header": {
        "background-color": "#1f4e78", "color": "white", "font-size": "17px", "font-weight": "bold", "text-align": "center"
    },
    ".ag-header-cell-label": {"justify-content": "center"},
    ".ag-cell": {"text-align": "center", "font-size": "16px", "display": "flex", "align-items": "center", "justify-content": "center"},
    ".ag-root-wrapper": {"border": "1px solid #ccc"}
}

grid_response2 = AgGrid(
    df_rekap,
    gridOptions=gb2.build(),
    custom_css=custom_css2,
    height=550,
    fit_columns_on_grid_load=True,
    use_container_width=True,
    editable=True
)

edited_df_rekap = grid_response2["data"]

# Tombol simpan CSV
if st.button("💾 Simpan Rekap Keuangan"):
    edited_df_rekap.to_csv("rekap_keuangan_juni.csv", index=False)
    st.success("✅ Data berhasil disimpan sebagai rekap_keuangan_juni.csv")

# Hitung total
def to_number(rp_string):
    if isinstance(rp_string, str):
        rp_string = rp_string.replace("Rp", "").replace(",", "").replace(".", "").strip()
        return int(rp_string) if rp_string.isdigit() else 0
    return 0

total_pemasukan = sum([to_number(val) for val in edited_df_rekap["Jumlah Pemasukan"]])
total_pengeluaran = sum([to_number(val) for val in edited_df_rekap["Jumlah Pengeluaran"]])
total_nominal = sum([to_number(val) for val in edited_df_rekap["Nominal"]])

# Tampilkan total pemasukan & pengeluaran
st.markdown(
    f"""
    <div style="text-align: center;">
        <h2>🧾 Rekap Total</h2>
        <div style="display: flex; justify-content: center; gap: 80px; font-size: 24px;">
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 12px;">
                <strong>💰 Total Pemasukan</strong><br>{format_rp(total_pemasukan)}
            </div>
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 12px;">
                <strong>💸 Total Pengeluaran</strong><br>{format_rp(total_pengeluaran)}
            </div>
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 12px;">
                <strong>📦 Total Rincian Biaya</strong><br>{format_rp(total_nominal)}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Hitung saldo saat ini
saldo_saat_ini = total_pemasukan - (total_pengeluaran + total_nominal)

# Tampilkan saldo saat ini
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 30px;">
        <h3>💼 Saldo Saat Ini</h3>
        <div style="
            display: inline-block;
            background-color: #e6ffe6;
            padding: 25px 50px;
            border-radius: 14px;
            font-size: 28px;
            font-weight: bold;
            color: #006400;
            box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
        ">
            {format_rp(saldo_saat_ini)}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
