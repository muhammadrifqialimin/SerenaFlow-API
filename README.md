# 🧠 SereneFlow API

![Python](https://img.shields.io/badge/Python-v3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.109-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Security](https://img.shields.io/badge/AES--256-Encryption-success?style=flat-square&logo=security&logoColor=white)

**SereneFlow API** is a secure and intelligent backend service designed for mental health journaling and mood tracking. Built with a focus on privacy, it features **End-to-End Encryption** to ensure user journals remain confidential, alongside a robust mood tracking system powered by statistical analysis.

---

## 🌟 Key Features

- **🔐 End-to-End Encryption**: Utilizes **AES-256 (Fernet)** encryption for journal titles and content. Data is encrypted before saving to the database and decrypted only upon retrieval. Even database admins cannot read user journals.
- **🛡️ Secure Authentication**: Implements `Bcrypt` for password hashing and `JWT` (JSON Web Tokens) for stateless, secure user sessions.
- **📊 Smart Mood Tracker**: Leverages **PostgreSQL JSON Columns** to store flexible mood tags and integer-based scoring for precise emotional tracking.
- **📈 Analytics & Statistics**: Built-in endpoints to calculate average mood scores, track total logs, and visualize recent emotional trends (Data Analytics).
- **🚀 Scalable Architecture**: Follows a modular structure with FastAPI routers, Pydantic schemas, and Dependency Injection.

---

## 🛠 Tech Stack

| Component       | Technology   | Description                                      |
| :-------------- | :----------- | :------------------------------------------------|
| **Language**    | Python 3.12+ | High-level programming language                  |
| **Framework**   | FastAPI      | Modern, fast (high-performance) web framework    |
| **Database**    | PostgreSQL   | Advanced relational database with JSON support   |
| **ORM**         | SQLAlchemy   | Python SQL toolkit and Object Relational Mapper  |
| **Security**    | Cryptography | Library for AES-256 encryption & decryption      |
| **Auth**        | JWT & Bcrypt | Token-based auth & Password hashing              |
| **Validation**  | Pydantic     | Data validation and settings management          |

---

## 📂 Project Structure

This project follows a modular architecture for better maintainability and scalability.

```bash
sereneflow-api/
│
├── app/
│   ├── core/           # Configuration, Security, & Database Connection
│   ├── models/         # SQLAlchemy Database Models
│   ├── routers/        # API Endpoints (Auth, Journals, Moods)
│   ├── schemas/        # Pydantic Schemas (Request/Response Validation)
│   ├── dependencies.py # Auth Dependencies (get_current_user)
│   └── main.py         # App Entry Point
├── venv/               # Virtual Environment
├── .env                # Environment Variables
├── requirements.txt    # Project Dependencies
└── README.md           # Documentation
```

## 🚀 Getting Started
Follow these steps to run the project locally.

1. **Prerequisites\***
   Make sure you have installed:

Python (v3.10 or higher)

PostgreSQL

2. **Clone the Repository**

```bash
git clone [https://github.com/muhammadrifqialimin/SerenaFlow-API.git](https://github.com/muhammadrifqialimin/SerenaFlow-API.git)
cd SereneFlow-API
```

3. **Set Up Virtual Environment**

```bash
# Create Virtual Environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```


4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure Environment Variables**
  Create a `.env` file in the root directory and add the following variables:

```env
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/sereneflow_db"
SECRET_KEY="your_secret_key_here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. **Start the Server**

```bash
uvicorn app.main:app --reload
```

the server will start at: `http://127.0.0.1:8000`
Swagger UI Documentation: `http://127.0.0.1:8000/docs`

## 🔌 API Documentation
You can test these endpoints using Swagger UI, Postman, or cURL.

### 🔐 Authentication

1. **Register User**

- URL: `POST /auth/register`
- Body:

```JSON
{
  "email": "rifqi@umy.ac.id",
  "password": "securepassword"
}
```

2. **Login User**

- URL: `POST /auth/login`
Response: Returns a `access_token`. Use this token for subsequent requests.

### 📖 Encrypted Journals

1. **Create Journal**

- URL: `POST /journals/`
- Auth: Bearer Token
-Body:

```JSON
{
  "title": "My Secret Day",
  "content": "Nobody can read this except me."
}
```

2. **Get My Journals**

- URL: `GET /journals/`
- Auth: Bearer Token
- Description: Returns list of journals with decrypted content.

### 🎭 Mood Tracker & Analytics

1. **Log Mood**

- URL: `POST /moods/`
- Auth: Bearer Token
- Response:

```JSON
{
  "total_logs": 15,
  "average_score": 7.5,
  "recent_trend": [8, 9, 6, 7, 8]
}
```

## 👨‍💻 Author

**Muhammad Rifqi Alimin**
