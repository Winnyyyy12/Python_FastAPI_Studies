from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="Hospital Appointment System (Query Parameters Only)")

# ---------------------------
# Data Models
# ---------------------------
class Doctor(BaseModel):
    id: int
    name: str
    specialization: str

class Appointment(BaseModel):
    id: int
    patient_name: str
    doctor_id: int
    date: str
    status: str  # pending, confirmed, cancelled


# ---------------------------
# Dummy Data Storage
# ---------------------------
doctors: List[Doctor] = [
    Doctor(id=1, name="Dr. Winny", specialization="Cardiologist"),
    Doctor(id=2, name="Dr. Junie", specialization="Dentist"),
    Doctor(id=3, name="Dr. Sheeba", specialization="Neurologist")
]

appointments: List[Appointment] = []


# ---------------------------
# Doctor Endpoints
# ---------------------------

@app.get("/doctors")
def get_doctors(
    specialization: Optional[str] = Query(None, description="Filter doctors by specialization")):
    if specialization:
        result = [d for d in doctors if d.specialization.lower() == specialization.lower()]
    else:
        result = doctors

    if not result:
        raise HTTPException(status_code=404, detail="No doctors found.")
    return result


@app.post("/doctors")
def add_doctor(
    name: str = Query(description="Doctor's name"),
    specialization: str = Query(description="Doctor's specialization")):
    doctor_id = len(doctors) + 1
    new_doctor = Doctor(id=doctor_id, name=name, specialization=specialization)
    doctors.append(new_doctor)
    return {"message": "Doctor added successfully", "doctor": new_doctor}


@app.delete("/doctors")
def delete_doctor(doctor_id: int = Query(description="Doctor ID to delete")):
    for d in doctors:
        if d.id == doctor_id:
            doctors.remove(d)
            return {"message": "Doctor deleted successfully"}
    raise HTTPException(status_code=404, detail="Doctor not found")


# ---------------------------
# Appointment Endpoints
# ---------------------------

@app.get("/appointments")
def get_appointments(
    doctor_id: Optional[int] = Query(None, description="Filter by doctor ID"),
    status: Optional[str] = Query(None, description="Filter by appointment status")):
    results = appointments

    if doctor_id is not None:
        results = [a for a in results if a.doctor_id == doctor_id]
    if status is not None:
        results = [a for a in results if a.status.lower() == status.lower()]

    if not results:
        raise HTTPException(status_code=404, detail="No matching appointments found.")
    return results


@app.post("/appointments")
def create_appointment(
    patient_name: str = Query( description="Patient name"),
    doctor_id: int = Query(description="Doctor ID"),
    date: str = Query(description="Appointment date (YYYY-MM-DD)")):
    # Validate doctor exists
    if not any(d.id == doctor_id for d in doctors):
        raise HTTPException(status_code=400, detail="Invalid doctor ID")

    appointment_id = len(appointments) + 1
    new_appointment = Appointment(
        id=appointment_id,
        patient_name=patient_name,
        doctor_id=doctor_id,
        date=date,
        status="pending"
    )
    appointments.append(new_appointment)
    return {"message": "Appointment created successfully", "appointment": new_appointment}


@app.put("/appointments")
def update_appointment(
    appointment_id: int = Query(description="Appointment ID to update"),
    status: str = Query(description="New status (pending/confirmed/cancelled)")):
    for a in appointments:
        if a.id == appointment_id:
            a.status = status
            return {"message": "Appointment updated successfully", "appointment": a}
    raise HTTPException(status_code=404, detail="Appointment not found")


@app.delete("/appointments")
def delete_appointment(appointment_id: int = Query(description="Appointment ID to delete")):
    for a in appointments:
        if a.id == appointment_id:
            appointments.remove(a)
            return {"message": "Appointment deleted successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")
