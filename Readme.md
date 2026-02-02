# Chemical Equipment Analyzer Project

A full-stack web application with Django backend and React/TypeScript frontend, featuring equipment data management and reporting capabilities.

## Project Structure

```
Project/
├── backend/          # Django REST API
│   ├── api/         # Main app with models, views, serializers
│   ├── manage.py
│   └── requirements.txt
└── frontend/        # React & Desktop applications
    ├── website/     # React TypeScript web app (Vite)
    └── desktop_app/ # Python desktop app (Pyqt)
```

## Backend Setup

1. Navigate to `backend/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Frontend Setup

### Web Application
```bash
cd frontend/website
npm install
npm run dev
```

### Desktop Application
```bash
cd frontend/desktop_app
pip install -r requirements.txt
python main.py
```

## Features

- User authentication (signup/login)
- Equipment data upload and management
- CSV file processing
- Dashboard with data visualization
- Report generation

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: React, TypeScript, Vite
- **Desktop**: Python,PyQt
- **Database**: SQLite
