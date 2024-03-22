from pydantic import BaseModel

class Car(BaseModel):
    car_number: str

class ParkingSlot(BaseModel):
    car_number: str
    slot_number: int
