***

# ⚡ NATS & JetStream Edge Playground

A high-performance IIoT simulation stack demonstrating **NATS** as a modern alternative to MQTT for Edge Computing. This project features a resilient data pipeline from a simulated sensor to **TimescaleDB** with real-time visualization in **Grafana**.



---

## 🏗️ Architecture Overview

1.  **NATS Server:** The central nervous system. Unlike traditional brokers, NATS uses a lightweight "Subject" system and supports **JetStream** for persistent messaging.
2.  **TimescaleDB:** An open-source time-series database optimized for fast ingestion and complex SQL queries.
3.  **Python Logic (Async):** A single asynchronous service that acts as both:
    * **Producer:** Simulates an industrial sensor publishing to `factory.sensor.temperature`.
    * **Consumer:** Subscribes to the subject and handles database persistence.
4.  **Grafana:** Provides the visual monitoring layer for the ingested telemetry.

---

## 📂 Project Structure

```text
NATS_PLAYGROUND/
├── database/
│   └── init-db.sql          # SQL schema & Hypertable initialization
├── scripts/
│   ├── Dockerfile           # Python environment (nats-py + psycopg2)
│   └── nats_app.py          # Asynchronous NATS logic
├── Makefile                 # Command shortcuts
└── docker-compose.yml       # Full stack orchestration
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Docker** and **Make** installed.

### 2. Build and Launch
Run the following command to build the Python logic and start all services:
```bash
make build
```

### 3. Verify Data Flow
You can monitor the logs to see the "Producer" and "Consumer" in action:
```bash
make logs
```

### 4. Check the Database
Query the TimescaleDB directly to see the time-series records:
```bash
make db-shell
# Inside the shell, run:
SELECT * FROM nats_data ORDER BY time DESC LIMIT 10;
```

---

## 🔬 Learning: NATS vs. MQTT

| Feature | MQTT (Standard) | NATS |
| :--- | :--- | :--- |
| **Routing** | Hierarchy with `/` (factory/sensor) | Hierarchy with `.` (factory.sensor) |
| **Wildcards** | `+` and `#` | `*` and `>` |
| **Delivery** | Push-only | Push or Pull (JetStream) |
| **State** | Retained Messages / LWT | Key-Value Store / JetStream |
| **Speed** | High | Ultra-High (Lower latency) |



---

## 📊 Dashboard Setup (Grafana)

1.  Navigate to `http://localhost:3000` (User: `admin` / Pass: `admin`).
2.  **Data Source:** Add **PostgreSQL**.
    * **Host:** `timescaledb:5432`
    * **User/Pass:** `postgres` / `password`
    * **SSL:** `disable`
3.  **Visual:** Create a new dashboard with this query:
    ```sql
    SELECT time, value, subject 
    FROM nats_data 
    WHERE $__timeFilter(time) 
    ORDER BY time ASC;
    ```

---

## 🛠️ Makefile Commands

| Command | Action |
| :--- | :--- |
| `make build` | Rebuilds the logic app and starts the stack. |
| `make up` | Starts the containers in the background. |
| `make logs` | Follows the Python application logs. |
| `make db-shell` | Opens the Postgres terminal. |
| `make down` | Stops the containers. |
| `make clean` | **Destructive:** Wipes containers and all database data. |

---

## 📚 Advanced Challenges
* **Persistent Storage:** Research how to convert the `nats_app.py` to use a **Durable Consumer**. This ensures that even if the Python app crashes, it will "catch up" on all missed data once it restarts.
* **NATS Monitoring:** Visit `http://localhost:8222` to view the internal NATS server statistics and message rates.