# chronicle-technical-test
Back End Technical Test for Back End Internship at Chronicle

# Distributed E-Commerce Order System

A scalable backend API for handling product sales and order processing. This system ensures data consistency during high-concurrency stock updates and offloads processing tasks to background workers.

## Tech Stack
* **Framework:** FastAPI (Python 3.12)
* **Database:** PostgreSQL 15
* **Queue/Caching:** Redis 7
* **Worker:** Celery
* **Containerization:** Docker & Docker Compose

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/allegrafs066/chronicle-technical-test
    cd chronicle-technical-test
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the API:**
    * **Swagger UI:** http://localhost:8000/docs
    * **API Root:** http://localhost:8000

4.  **Postman Collection:**
    * **.JSON file is in the repo or access it through this link:** https://gold-astronaut-108218.postman.co/workspace/Chronicle-Technical-Test~b3af657d-7b50-44bf-8bbb-96be1a0e130d/collection/34723443-65c9f60d-a055-48ed-8105-e723066837bf?action=share&creator=34723443

## Architecture Decisions

### Race Condition Handling (Stock Validation)
To prevent overselling when multiple users purchase the same item simultaneously, I implemented **Pessimistic Locking** using SQLAlchemy's `with_for_update()`.

* **Mechanism:** When an order request begins, the specific product row is locked in the database (`SELECT ... FOR UPDATE`).
* **Result:** Concurrent requests are forced to wait until the lock is released (after transaction commit). This guarantees that the stock check (`if stock < quantity`) is always performed on the most up-to-date data.

### Caching Strategy
* **Read:** Product details are cached in Redis for 5 minutes to reduce DB load.
* **Invalidation:** The cache for a specific product is automatically invalidated (deleted) whenever stock is updated or product details are changed.

### Background Processing
* **Order Processing:** Upon successful order creation, the order ID is pushed to a Celery queue. The worker picks up the task asynchronously to simulate downstream processing (e.g., shipping logistics or email notifications) without blocking the HTTP response.