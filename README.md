# 📚 Interview Question Bank

A full-stack web app to store, search and review your interview questions.
Uses **SQLite** for storage and **Flask** for the backend.

---

## 🚀 Run locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the app
```bash
python app.py
```

### 3. Open browser
→ http://127.0.0.1:5000

Your database is created automatically as `questions.db` next to `app.py`.

---

## 🌐 Deploy to Render (free hosting)

Render gives you a free live URL so you can use your app from anywhere.

### Step 1 — Push to GitHub
1. Create a new repo on github.com
2. In your project folder:
```bash
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/YOUR_USERNAME/interview-bank.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Fill in:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn wsgi:app`
   - **Environment:** Python 3

### Step 3 — Add a Persistent Disk (important!)
Without a disk, your data resets on every deploy.

1. In your Render service → **Disks** tab
2. Add disk:
   - Mount path: `/data`
   - Size: 1 GB (free tier)
3. Add environment variable:
   - `DATA_DIR` = `/data`

### Step 4 — Deploy
Click **Deploy**. Your app will be live at `https://your-app.onrender.com` 🎉

---

## 📁 File structure
```
interview_bank/
├── app.py              ← Flask backend + SQLite
├── wsgi.py             ← Gunicorn entry point
├── requirements.txt    ← flask, gunicorn
├── Procfile            ← for Render/Heroku
├── render.yaml         ← Render auto-config
├── .env.example        ← Environment variable template
└── templates/
    └── index.html      ← Full frontend UI
```

---

## ⚙️ Environment variables

| Variable   | Default     | Description                        |
|------------|-------------|------------------------------------|
| `DATA_DIR` | `.` (local) | Folder where questions.db is saved |

Set `DATA_DIR=/data` on Render so data persists across deploys.
