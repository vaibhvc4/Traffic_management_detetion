import mysql.connector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
config = {
    "host": "localhost",
    "user": "vaibhav",
    "password": "vaibhav@123__",
    "database": "vaibhav2",
    'auth_plugin': 'mysql_native_password'
}
conn = mysql.connector.connect(**config)

cursor = conn.cursor()
cursor1 = conn.cursor()
class VehicleData(BaseModel):
    vehicle_no: str

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:['*']",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post('/vehicle_number')
async def vehicle_number(data: VehicleData):
    vehicle_no = data.vehicle_no
    query = 'SELECT * FROM violations where vehicle_no=%s'
    cursor.execute(query, (vehicle_no,))  
    result1 = cursor.fetchall()
    query = 'SELECT * FROM payments where vehicle_no=%s'
    cursor1.execute(query, (vehicle_no,))  
    result2 = cursor1.fetchall()
    print(result2)
    json = {'violation': result1 ,'payments':result2}
    print(json)
    return json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
