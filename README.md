# Secure Socket Chat

A minimal command-line chat application built using Python's `socket`, `ssl`, and `threading` libraries. It enables encrypted communication between multiple clients via a central server.


## Setup

### 1. Generate SSL Certificate

Before starting the server, generate the `cert.pem` and `key.pem`:

- This creates a **self-signed** certificate valid for `localhost`.

```bash
python3 generate_cert.py
```
> Make sure to change the parameters inside the file if you'd like

OR

```bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365
```

### 2. Start the Server

```bash
python3 server.py
```

### 3. Start a Client

In a **new terminal**, run:

```bash
python3 client.py
```
Repeat in other terminals to simulate multiple users.

## 🗂 Files

| File              | Description                             |
|-------------------|-----------------------------------------|
| `server.py`       | Runs the chat server with SSL support   |
| `client.py`       | Connects to the server and handles chat |
| `generate_cert.py`| Generates `key.pem` and `cert.pem` using Python's `cryptography` module |


