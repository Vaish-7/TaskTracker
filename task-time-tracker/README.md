# Time Tracker

**A simple task tracker to record start/stop times and compute durations for individual tasks.**  
Its built with Python + Flask (REST API), SQLite (persistence), and a minimal HTML/CSS/JS frontend. Designed to be Git‑friendly and easy to extend with CI/CD later.

---

## Table of Contents
- **Overview**
- **Architecture**
- **Features**
- **Tech Stack**
- **Project Layout**
- **Quick Start**
- **API Reference**
- **Database Schema**
- **Development Plan**
- **Testing**
- **CI CD Notes**
- **Contributing**
- **License**

---

## Overview
This project records the lifecycle of tasks (create, start, stop, update, delete) and computes elapsed durations.

---

## Architecture
**Three layered architecture**

- **Frontend** — HTML, CSS, JavaScript;.  
- **API** — Flask REST API that serves the frontend and exposes CRUD endpoints for tasks.  
- **Database** — SQLite for development; schema stores `id`, `name`, `start_time`, `end_time`, `duration_seconds`, `status`, `notes`.

---

## Features
- Create tasks with optional notes.  
- Start and stop timers for tasks.  
- Automatic duration calculation.  
- List, update, and delete tasks.  
- Filter tasks by status (running, stopped, completed).  
- Simple export/migration friendly data model.

---

## Tech Stack
- **Frontend:** HTML, CSS
- **Backend:** Python, Flask, Flask Blueprints, SQLAlchemy  
- **Database:** SQLite (file)  
- **Dev tools:** VS Code, `venv`, `pip`, Git

---

## Project Layout
        time-tracker/
        ├─ README.md
        ├─ requirements.txt
        ├─ venv/ (virtual env)
        ├─ app/
        │  ├─ init.py
        │  ├─ errors.py       
        │  ├─ models.py
        │  ├─ routes.py
        │  ├─ db.py
        │  ├─ static/
        │  │  └─ styles.css
        │  └─ templates/
        │     ├─ register.html
        |     ├─ login.html
        |     ├─ logout.html
        |     ├─ profile.html
        |     ├─ dashboard.html
        |     ├─ 403.html
        |     ├─ 404.html
        |     └─ 500.html
        └─ main.py