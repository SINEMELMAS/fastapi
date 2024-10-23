from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import sqlite3
from typing import List
from contextlib import asynccontextmanager

app = FastAPI()

# Pydantic modeli (Veri doğrulaması dahil)
class MachineData(BaseModel):
    machineID: int
    footfall: int
    tempMode: int
    AQ: float
    USS: float
    CS: float
    VOC: float
    RP: float
    IP: float
    Temperature: float
    fail: bool

    # Pydantic V2 doğrulamalar
    @field_validator('footfall', 'tempMode')
    def check_positive(cls, value):
        if value < 0:
            raise ValueError(f'{cls.__name__} must be a non-negative value')
        return value

# Veritabanı bağlantısı açma
def get_db_connection():
    try:
        conn = sqlite3.connect('machine_data.db')
        conn.row_factory = sqlite3.Row  # Veriyi dict olarak döndürür
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database connection failed")

# Veritabanı tablosunu oluşturma
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS machines (
        machineID INTEGER PRIMARY KEY,
        footfall INTEGER,
        tempMode INTEGER,
        AQ REAL,
        USS REAL,
        CS REAL,
        VOC REAL,
        RP REAL,
        IP REAL,
        Temperature REAL,
        fail BOOLEAN
    )
    ''')
    conn.commit()
    conn.close()

# Başlangıç verilerini ekleme
def insert_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Veritabanında zaten veri var mı kontrolü
    cursor.execute("SELECT COUNT(*) FROM machines")
    count = cursor.fetchone()[0]

    if count == 0:  # Eğer tablo boşsa verileri ekle
        data = [
            (1, 0, 7, 7, 1, 6, 6, 36, 3, 1, 1),
            (2, 190, 1, 3, 3, 5, 1, 20, 4, 1, 0),
            (3, 31, 7, 2, 2, 6, 1, 24, 6, 1, 0),
            (4, 83, 4, 3, 4, 5, 1, 28, 6, 1, 0),
            (5, 640, 7, 5, 6, 4, 0, 68, 6, 1, 0),
            (6, 110, 3, 3, 4, 6, 1, 21, 4, 1, 0),
            (7, 100, 7, 5, 6, 4, 1, 77, 4, 1, 0),
            (8, 31, 1, 5, 4, 5, 4, 21, 4, 1, 0),
            (9, 180, 7, 4, 6, 3, 3, 31, 4, 1, 0),
            (10, 2800, 0, 3, 3, 7, 0, 39, 3, 1, 0)
        ]

        cursor.executemany('INSERT INTO machines VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        conn.commit()

    conn.close()

# Yaşam döngüsü yönetimi (Veritabanını başlatma)
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    insert_initial_data()
    yield  # Servis çalışmaya devam eder

# FastAPI'yi yaşam döngüsü ile başlatma
app = FastAPI(lifespan=lifespan)

# Tüm makineleri listeleme (GET)
@app.get("/machines/", response_model=List[MachineData])
def get_all_machines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machines")
    machines = cursor.fetchall()
    conn.close()
    return [dict(machine) for machine in machines]

# Belirli bir makineyi ID ile getirme (GET)
@app.get("/machines/{machine_id}", response_model=MachineData)
def get_machine(machine_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machines WHERE machineID = ?", (machine_id,))
    machine = cursor.fetchone()
    conn.close()
    if machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return dict(machine)

# Yeni bir makine ekleme (POST)
@app.post("/machines/", response_model=MachineData)
def add_machine(machine: MachineData):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO machines (machineID, footfall, tempMode, AQ, USS, CS, VOC, RP, IP, Temperature, fail) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (machine.machineID, machine.footfall, machine.tempMode, machine.AQ, machine.USS, machine.CS, machine.VOC,
         machine.RP, machine.IP, machine.Temperature, machine.fail)
    )
    conn.commit()
    conn.close()
    return machine

# Bir makineyi güncelleme (PUT)
@app.put("/machines/{machine_id}", response_model=MachineData)
def update_machine(machine_id: int, updated_machine: MachineData):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Güncellemeden önce makine var mı kontrolü
    cursor.execute("SELECT * FROM machines WHERE machineID = ?", (machine_id,))
    machine = cursor.fetchone()
    if machine is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Machine not found")

    cursor.execute(
        "UPDATE machines SET footfall = ?, tempMode = ?, AQ = ?, USS = ?, CS = ?, VOC = ?, RP = ?, IP = ?, Temperature = ?, fail = ? WHERE machineID = ?",
        (
        updated_machine.footfall, updated_machine.tempMode, updated_machine.AQ, updated_machine.USS, updated_machine.CS,
        updated_machine.VOC, updated_machine.RP, updated_machine.IP, updated_machine.Temperature, updated_machine.fail,
        machine_id)
    )
    conn.commit()
    conn.close()

    return updated_machine

# Bir makineyi silme (DELETE)
@app.delete("/machines/{machine_id}")
def delete_machine(machine_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Silmeden önce makine var mı kontrolü
    cursor.execute("SELECT * FROM machines WHERE machineID = ?", (machine_id,))
    machine = cursor.fetchone()
    if machine is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Machine not found")

    cursor.execute("DELETE FROM machines WHERE machineID = ?", (machine_id,))
    conn.commit()
    conn.close()

    return {"message": "Machine deleted successfully"}
