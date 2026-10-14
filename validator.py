import sqlite3
import pandas as pd

def validate_timesheet():
    db_name = "mcr_data.db"
    output_excel = "anomali_timesheet_untuk_BAST.xlsx"

    # Connect to SQLite database
    conn = sqlite3.connect(db_name)

    # SQL query to find rows where jam_kerja_dilaporkan != (hm_akhir - hm_awal)
    query = """
    SELECT
        t.id AS timesheet_id,
        u.nama_unit,
        u.jenis_unit,
        u.status_aktivitas,
        t.tanggal,
        t.hm_awal,
        t.hm_akhir,
        (t.hm_akhir - t.hm_awal) AS hm_selisih,
        t.jam_kerja_dilaporkan,
        ROUND(t.jam_kerja_dilaporkan - (t.hm_akhir - t.hm_awal), 1) AS selisih_anomali
    FROM timesheet t
    JOIN unit_rental u ON t.id_unit = u.id
    WHERE ABS(t.jam_kerja_dilaporkan - (t.hm_akhir - t.hm_awal)) > 0.01;
    """

    # Read query results into a pandas DataFrame
    df_anomalies = pd.read_sql_query(query, conn)
    conn.close()

    print(f"Ditemukan {len(df_anomalies)} baris data anomali timesheet.")
    print(df_anomalies)

    # Export to Excel using pandas & openpyxl
    if not df_anomalies.empty:
        df_anomalies.to_excel(output_excel, index=False, sheet_name="Anomali BAST")
        print(f"Data anomali berhasil diekspor ke '{output_excel}'.")
    else:
        print("Tidak ada data anomali yang ditemukan.")

if __name__ == "__main__":
    validate_timesheet()
