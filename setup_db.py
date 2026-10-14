import sqlite3
import random
from datetime import datetime, timedelta

def setup_database():
    db_name = "mcr_data.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop tables if they already exist for clean setup
    cursor.execute("DROP TABLE IF EXISTS timesheet;")
    cursor.execute("DROP TABLE IF EXISTS unit_rental;")

    # 1. Create unit_rental table
    cursor.execute("""
    CREATE TABLE unit_rental (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_unit TEXT NOT NULL,
        jenis_unit TEXT NOT NULL,
        status_aktivitas TEXT NOT NULL
    );
    """)

    # 2. Create timesheet table
    cursor.execute("""
    CREATE TABLE timesheet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_unit INTEGER,
        tanggal TEXT,
        jam_kerja_dilaporkan REAL,
        hm_awal REAL,
        hm_akhir REAL,
        FOREIGN KEY (id_unit) REFERENCES unit_rental (id)
    );
    """)

    # Generate 30 unit_rental dummy data
    jenis_list = ["Excavator", "Dump Truck", "Bulldozer", "Grader", "Wheel Loader"]
    status_list = ["Operasi", "Standby", "Breakdown"]

    units = []
    for i in range(1, 31):
        nama = f"UNIT-{i:03d}"
        jenis = random.choice(jenis_list)
        status = random.choice(status_list)
        units.append((nama, jenis, status))

    cursor.executemany("""
    INSERT INTO unit_rental (nama_unit, jenis_unit, status_aktivitas)
    VALUES (?, ?, ?);
    """, units)
    conn.commit()

    # Fetch inserted unit IDs
    cursor.execute("SELECT id FROM unit_rental;")
    unit_ids = [row[0] for row in cursor.fetchall()]

    # Generate timesheet dummy data (~60 rows)
    # We will deliberately make 5 rows mismatched (anomalies)
    base_date = datetime(2026, 10, 1)
    timesheet_data = []

    # Let's pick 5 random indices for anomaly out of 60 total rows
    total_rows = 60
    anomaly_indices = set(random.sample(range(total_rows), 5))

    for idx in range(total_rows):
        u_id = random.choice(unit_ids)
        days_offset = random.randint(0, 10)
        tanggal = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")

        hm_awal = round(random.uniform(1000.0, 5000.0), 1)
        actual_diff = round(random.uniform(5.0, 14.0), 1)
        hm_akhir = round(hm_awal + actual_diff, 1)

        if idx in anomaly_indices:
            # Create a mismatch: reported hours differs from hm_akhir - hm_awal
            mismatch_delta = random.choice([-3.0, -2.0, 2.5, 4.0, 5.0])
            jam_kerja_dilaporkan = round(actual_diff + mismatch_delta, 1)
            if jam_kerja_dilaporkan < 0:
                jam_kerja_dilaporkan = 0.0
        else:
            jam_kerja_dilaporkan = actual_diff

        timesheet_data.append((u_id, tanggal, jam_kerja_dilaporkan, hm_awal, hm_akhir))

    cursor.executemany("""
    INSERT INTO timesheet (id_unit, tanggal, jam_kerja_dilaporkan, hm_awal, hm_akhir)
    VALUES (?, ?, ?, ?, ?);
    """, timesheet_data)
    conn.commit()

    print(f"Database '{db_name}' successfully created and populated.")
    print(f"- 30 units inserted into 'unit_rental'.")
    print(f"- {total_rows} timesheet entries inserted (including exactly 5 anomaly rows).")

    # Display anomaly rows for verification
    cursor.execute("""
    SELECT t.id, u.nama_unit, t.tanggal, t.jam_kerja_dilaporkan, t.hm_awal, t.hm_akhir, (t.hm_akhir - t.hm_awal) AS hm_diff
    FROM timesheet t
    JOIN unit_rental u ON t.id_unit = u.id
    WHERE ABS(t.jam_kerja_dilaporkan - (t.hm_akhir - t.hm_awal)) > 0.01;
    """)
    anomalies = cursor.fetchall()
    print("\nVerified Anomaly Rows in Timesheet:")
    for anom in anomalies:
        print(f"Timesheet ID: {anom[0]}, Unit: {anom[1]}, Date: {anom[2]}, Reported: {anom[3]}, HM Diff: {anom[5] - anom[4]:.1f}")

    conn.close()

if __name__ == "__main__":
    setup_database()
