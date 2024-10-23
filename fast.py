from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

class Machine(BaseModel):
    machineID: Optional[int]  # Optional for POST requests
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


def setup_database():
    try:
        conn = sqlite3.connect('machine_data.db')  # Create a connection to the database
        cursor = conn.cursor()  # Create a cursor
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            machineID INTEGER PRIMARY KEY AUTOINCREMENT,
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
        conn.commit()  # Save changes
        conn.close()  # Close the connection
    except sqlite3.Error as e:  # Handle potential errors
        print(e)


setup_database()


@app.get("/machines/", response_model=List[Machine])
async def read_machines(limit: int = 10):
    try:
        conn = sqlite3.connect('machine_data.db')  # Create a connection to the database
        cursor = conn.cursor()  # Create a cursor to interact with the database
        cursor.execute("SELECT * FROM machines LIMIT ?", (limit,))  # Fetch limited rows from the machines table
        rows = cursor.fetchall()  # Fetch all results from the database
        conn.close()  # Close the database connection

        # Convert rows to a list of Machine instances
        return [Machine(machineID=row[0], footfall=row[1], tempMode=row[2], AQ=row[3], USS=row[4], CS=row[5], VOC=row[6], RP=row[7], IP=row[8], Temperature=row[9], fail=bool(row[10])) for row in rows]
    except sqlite3.Error as e:  # Handle potential errors
        print(e)
        raise HTTPException(status_code=500, detail="Failed to fetch machines")  # Return an error message


@app.post("/machines/", response_model=Machine)
async def create_machine(machine: Machine):
    try:
        conn = sqlite3.connect('machine_data.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO machines (footfall, tempMode, AQ, USS, CS, VOC, RP, IP, Temperature, fail) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (machine.footfall, machine.tempMode, machine.AQ, machine.USS, machine.CS, machine.VOC, machine.RP, machine.IP, machine.Temperature, machine.fail)
        )
        conn.commit()
        machine.machineID = cursor.lastrowid  # Get the ID of the newly inserted row
        conn.close()
        return machine  # Return the created machine
    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create machine")


@app.put("/machines/{machine_id}", response_model=Machine)
async def update_machine(machine_id: int, machine: Machine):
    try:
        conn = sqlite3.connect('machine_data.db')  # Create a connection to the database
        cursor = conn.cursor()  # Create a cursor
        cursor.execute(
            "UPDATE machines SET footfall = ?, tempMode = ?, AQ = ?, USS = ?, CS = ?, VOC = ?, RP = ?, IP = ?, Temperature = ?, fail = ? WHERE machineID = ?",
            (machine.footfall, machine.tempMode, machine.AQ, machine.USS, machine.CS, machine.VOC, machine.RP, machine.IP, machine.Temperature, machine.fail, machine_id)  # Use machineID for update
        )
        conn.commit()  # Save changes to the database
        conn.close()  # Close the connection
        return {**machine.dict(), "machineID": machine_id}  # Return the updated machine data
    except sqlite3.Error as e:  # In case of an error
        print(e)  # Print the error
        raise HTTPException(status_code=500, detail="Failed to update machine")  # Return an error message


@app.delete("/machines/{machine_id}")
async def delete_machine(machine_id: int):
    try:
        conn = sqlite3.connect('machine_data.db')  # Create a connection to the database
        cursor = conn.cursor()  # Create a cursor
        cursor.execute("DELETE FROM machines WHERE machineID = ?", (machine_id,))  # Execute an SQL query to delete a machine
        conn.commit()  # Save changes to the database
        conn.close()  # Close the connection
        return {"message": "Machine deleted"}  # Return a confirmation message of deletion
    except sqlite3.Error as e:  # In case of an error
        print(e)  # Print the error
        raise HTTPException(status_code=500, detail="Failed to delete machine")  # Return an error message
