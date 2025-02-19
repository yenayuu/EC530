### ** API DOCUMENTATION**

# **Smart Home API**
This API allows users to manage **users, houses, rooms, and smart devices** in a smart home system.

## ** 1. API Overview**
- **Technology Used**: FastAPI (Python)  
- **Purpose**: Manage users, houses, rooms, and IoT devices  
- **Features**:
  - User authentication (register, login)
  - CRUD operations for houses, rooms, and devices
  - Device control (e.g., turning lights on/off)
  - API error handling (validation, rate limiting, etc.)

### ** Base URL**
```
https://github.com/yenayuu/EC530.git
```


## ** 2. API Definitions**
This section describes the available **API endpoints**, the **expected input**, and the **returned response**.

### ** Users API**
#### ** Register a User**
- **Endpoint**: `POST /users/register`
- **Request Body (JSON)**:
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User registered successfully"
  }
  ```
- **Errors**:
  - `400 Bad Request`: "Email already registered"
  - `422 Unprocessable Entity`: "Invalid email format"

#### ** User Login**
- **Endpoint**: `POST /users/login`
- **Request Body (JSON)**:
  ```json
  {
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
  }
  ```
- **Errors**:
  - `401 Unauthorized`: "Incorrect password"
  - `404 Not Found`: "User not found"

---

### ** Houses API**
#### ** Create a House**
- **Endpoint**: `POST /houses`
- **Request Body (JSON)**:
  ```json
  {
    "name": "My Smart Home",
    "address": "123 Main Street"
  }
  ```
- **Response**:
  ```json
  {
    "message": "House created successfully",
    "house_id": 10
  }
  ```
- **Errors**:
  - `400 Bad Request`: "House with this name already exists"

#### ** Get House Details**
- **Endpoint**: `GET /houses/{house_id}`
- **Response**:
  ```json
  {
    "house_id": 10,
    "name": "My Smart Home",
    "address": "123 Main Street"
  }
  ```
- **Errors**:
  - `404 Not Found`: "House not found"

---

### ** Rooms API**
#### ** Add a Room**
- **Endpoint**: `POST /houses/{house_id}/rooms`
- **Request Body (JSON)**:
  ```json
  {
    "name": "Living Room",
    "room_type": "common"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Room added successfully",
    "room_id": 100
  }
  ```
- **Errors**:
  - `400 Bad Request`: "Invalid room type"

#### ** Get All Rooms in a House**
- **Endpoint**: `GET /houses/{house_id}/rooms`
- **Response**:
  ```json
  [
    {
      "room_id": 100,
      "name": "Living Room",
      "room_type": "common",
      "house_id": 10
    },
    {
      "room_id": 101,
      "name": "Bedroom",
      "room_type": "private",
      "house_id": 10
    }
  ]
  ```
- **Errors**:
  - `404 Not Found`: "No rooms found for this house"


### ** Devices API**
#### ** Add a Device**
- **Endpoint**: `POST /rooms/{room_id}/devices`
- **Request Body (JSON)**:
  ```json
  {
    "name": "Smart Light",
    "device_type": "light",
    "status": "off"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Device added successfully",
    "device_id": 200
  }
  ```
- **Errors**:
  - `400 Bad Request`: "Invalid device type"

#### ** Get All Devices in a Room**
- **Endpoint**: `GET /rooms/{room_id}/devices`
- **Response**:
  ```json
  [
    {
      "device_id": 200,
      "name": "Smart Light",
      "device_type": "light",
      "status": "off",
      "room_id": 100
    },
    {
      "device_id": 201,
      "name": "Smart Thermostat",
      "device_type": "thermostat",
      "status": "22°C",
      "room_id": 100
    }
  ]
  ```
- **Errors**:
  - `404 Not Found`: "No devices found in this room"


## ** 3. Data Structure**
The API uses the following **data structure models**:

| **Object**  | **Attributes** |
|------------|----------------------------------------|
| **User**   | `name` (string), `email` (string), `password` (string) |
| **House**  | `house_id` (int), `name` (string), `address` (string) |
| **Room**   | `room_id` (int), `house_id` (int), `name` (string), `room_type` (string) |
| **Device** | `device_id` (int), `room_id` (int), `name` (string), `device_type` (string), `status` (string) |


## ** 4. API Use Cases**
Here’s how the API can be used:

1. **User Registration & Login**  
   - Users sign up and log in to manage their smart home system.

2. **Managing Houses**  
   - Users can **create a house**, view **house details**, and manage multiple smart homes.

3. **Adding Rooms to a House**  
   - Each house can have different **rooms (e.g., Bedroom, Kitchen)**.

4. **Managing Smart Devices**  
   - Users can **add, update, and retrieve** smart home devices.

5. **Controlling Devices**  
   - Devices like **lights, thermostats, and cameras** can be turned on/off via API.

---

## ** 5. Running the API**
### ** Install Dependencies**
```bash
pip install fastapi uvicorn pydantic email-validator
```

### ** Run the API**
```bash
uvicorn src.main:app --reload
```

### ** Open API Docs**
After running, open **Swagger UI**:

```
https://github.com/yenayuu/EC530.git
```
