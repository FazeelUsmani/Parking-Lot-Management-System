from fastapi import APIRouter, HTTPException, Depends, status
from typing import Union
from ..models import Car, ParkingSlot
from ..config import settings
from ..database import get_slot_collection
from pymongo.collection import Collection

router = APIRouter()

@router.post("/park", response_model=ParkingSlot, status_code=status.HTTP_201_CREATED)
async def park_car(car: Car, slots_collection: Collection = Depends(get_slot_collection)):
    if slots_collection.find_one({"car_number": car.car_number}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Car is already parked.")

    # Find the first available slot
    for slot_number in range(1, settings.parking_lot_size + 1):
        if not slots_collection.find_one({"slot_number": slot_number}):
            break
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Parking lot is full.")

    parking_slot = {"car_number": car.car_number, "slot_number": slot_number}
    slots_collection.insert_one(parking_slot)
    return parking_slot

@router.delete("/unpark/{slot_number}", status_code=status.HTTP_200_OK)
async def unpark_car(slot_number: int, slots_collection: Collection = Depends(get_slot_collection)):
    result = slots_collection.find_one_and_delete({"slot_number": slot_number})
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot is empty or does not exist.")
    
    return {"message": f"Car {result['car_number']} has been removed from slot {slot_number}"}

@router.get("/getinfo", response_model=ParkingSlot)
async def get_info(car_number: Union[str, None] = None, slot_number: Union[int, None] = None, slots_collection: Collection = Depends(get_slot_collection)):
    query = {"car_number": car_number} if car_number else {"slot_number": slot_number}
    slot_info = slots_collection.find_one(query)
    
    if not slot_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car or slot not found.")
    
    return slot_info
