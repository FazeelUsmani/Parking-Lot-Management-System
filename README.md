# Parking Lot Management Server

This project implements a simple backend service for managing a parking lot using FastAPI and MongoDB. It provides a set of API endpoints to park and unpark cars, as well as to retrieve information about parked cars and their slots.

## Features

- Park a car in the parking lot.
- Unpark a car from the parking lot.
- Get information about a car or a slot in the parking lot.

## Installation

### Requirements

- Python 3.6+
- MongoDB
- pip

### Creating and Activating a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Dependency Installation

Before you can run the server, you need to install the required dependencies:

```bash
pip install fastapi uvicorn pymongo python-dotenv
```

#### Install MongoDB

```bash
brew tap mongodb/brew
brew install mongodb-community
```

#### Start MongoDB

```bash
brew services start mongodb/brew/mongodb-community
```

### Checking the Database Connection

To verify that your application is connected to MongoDB, you can check the connection status in your FastAPI code:

```python
@app.on_event("startup")
async def startup_db_client():
    try:
        # Attempt to fetch a document from the MongoDB server
        client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print("Failed to connect to MongoDB", e)
```

### Create an Environment Variable

1. Copy `.env.sample` to `.env`.

    ```bash
    cp .env.sample .env
    ```

2. Open the `.env` file in a text editor and set the `PARKING_LOT_SIZE` to your desired number of parking slots.

## Setup

1. Clone the repository to your local machine.
2. Copy `.env.sample` to `.env` and set your desired parking lot size.

    ```bash
    cp .env.sample .env
    # Edit .env to set the PARKING_LOT_SIZE
    ```

3. Ensure MongoDB is installed and running on your system.

## Running the Server

To start the server, run the following command:

```bash
uvicorn main:app --reload
```

## API Endpoints

### Park a Car

- **URL**: `/park`
- **Method**: `POST`
- **Body**: `{ "car_number": "car_number_value" }`
- **Success Response**: `200 OK` with JSON `{ "car_number": "car_number_value", "slot_number": slot_number_value }`
- **Error Response**: `400 Bad Request` if the parking lot is full.

### Unpark a Car

- **URL**: `/unpark`
- **Method**: `DELETE`
- **Body**: `{ "slot_number": slot_number_value }`
- **Success Response**: `200 OK` with JSON `{ "message": "Car car_number_value has been removed from slot slot_number_value" }`
- **Error Response**: `404 Not Found` if the slot is empty or does not exist.

### Get the Car/Slot Information

- **URL**: `/getinfo`
- **Method**: `GET`
- **Query Parameters**: `car_number=car_number_value` or `slot_number=slot_number_value`
- **Success Response**: `200 OK` with JSON `{ "car_number": "car_number_value", "slot_number": slot_number_value }`
- **Error Response**: `400 Bad Request` if neither car number nor slot number is provided, or `404 Not Found` if no matching car/slot is found.

## License

This project is licensed under the MIT License - see the LICENSE file for details.