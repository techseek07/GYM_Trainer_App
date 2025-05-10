# GitBud: AI-Powered Smart Gym Trainer API

GitBud is an intelligent fitness assistant that combines conversational AI with personalized workout and nutrition planning. Built with Flask and IBM Watson Assistant, it delivers a seamless API experience for fitness apps, health bots, or integrated wellness platforms.

---

## 🚀 Overview

GitBud acts as a backend engine to support gym users with:

- Personalized **workout schedules**
- Goal-based **nutritional meal plans**
- AI-enhanced interaction using **Watson Assistant**
- A scalable architecture ready for front-end or mobile app integration

---

## 🧠 Key Features

- **Natural Language Understanding**  
  Integrated with IBM Watson Assistant to interpret user intents.

- **Dynamic Meal Planning**  
  Recommends meals tailored for goals like muscle gain, weight loss, veganism, and more.

- **Workout Schedule Management**  
  Provides pre-defined or user-specific fitness schedules.

- **RESTful API Design**  
  Easy integration with mobile, web, or voice-based platforms.

- **Database Persistence**  
  Utilizes SQLite and SQLAlchemy for managing users and workouts.

---

## 🛠️ Technology Stack

| Layer        | Technology                  |
|--------------|------------------------------|
| Backend      | Flask (Python)               |
| AI Engine    | IBM Watson Assistant (V2 API)|
| ORM & DB     | SQLAlchemy + SQLite          |
| Web Security | Flask-CORS                   |
| Deployment   | Flask development server     |

---

## 🧩 Architecture

┌────────────┐ HTTP POST ┌─────────────────────┐
│ Client ├──────────────────────►│ /webhook │
└────────────┘ └────────┬─────────────┘
│
┌────────────────▼─────────────────┐
│ Intent Detection (Watson NLP) │
└────────────────┬─────────────────┘
│
┌─────────────────────────────┴──────────────────────────────┐
│ Meal Plan Logic + User Schedule DB │
└─────────────────────────────┬──────────────────────────────┘
│
┌─────────────▼─────────────┐
│ JSON Response │
└────────────────────────────┘

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gitbud.git
   cd gitbud
    ```
### 2.Create a virtual environment and install dependencies:
   ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

   ```
### 3.Ensure fitness.db exists or initialize it:
   ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

   ```
### 4.Run the app::
   ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

   ```
