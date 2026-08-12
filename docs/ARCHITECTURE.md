# SYSTEM ARCHITECTURE
  FIG 1.0.0.0

  ```Plaintext
                        +---------------------------------------+
                        |           Client Application          |
                        +------------------- +------------------+
                                             |
                                   HTTP POST /api/v1/invoices
                                             |
                                             v
                        +---------------------------------------+
                        |            Nginx Proxy                |
                        |      (SSL / Rate-Limiting)            |
                        +--------------------+------------------+
                                             |
                                             v
                        +---------------------------------------+
                        |          FastAPI App Engine           |
                        |   - API Key Security Check            |
                        |   - Pydantic Payload Validation       |
                        +--------------------+------------------+
                                             |
                     +-----------------------+-----------------------+
                     |                                               |
                     v                                               v
       +---------------------------+                   +------------------------------+
       |   PostgreSQL Database     |                   |    Async Background Worker   |
       |  (Persist Order Record)   |                   |    (FastAPI Tasks/Celery)    |
       +---------------------------+                   +-------------+----------------+
                                                                     |
                                                                     v
                                             +-----------------------+-----------------------+
                                             |                                               |
                                             v                                               v
                               +---------------------------+                   +---------------------------+
                               |   PDF Rendering Engine    |                   |   SMTP Mail Service       |
                               |    (Jinja2 + HTML/CSS)    |                   |  (Attach PDF & Email)     |
                               +-------------+-------------+                   +---------------------------+
                                             |
                                             v
                               +---------------------------+
                               |    Local / S3 Storage     |
                               |   (Store Generated PDF)   |
                               +---------------------------+
```
