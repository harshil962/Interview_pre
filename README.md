# 📚 Interview Question Bank

A local web app to store and review your interview questions.

## ✅ Features
- Add MCQ, Theory, Practical, Technical questions
- Store company name, interview round, date, and tags
- MCQ with 4 options + mark correct answer
- Show/hide answers
- Bookmark important questions
- Search by keyword, tag, or company
- Filter by type or company
- Sort by newest/oldest/company/A-Z
- Stats dashboard
- All data saved in questions.json (your laptop, no internet needed)

---

## 🚀 How to Run

### Step 1 — Make sure Python is installed
Open terminal / command prompt and run:
```
python --version
```
You need Python 3.7 or higher.

### Step 2 — Install Flask
```
pip install flask
```

### Step 3 — Run the app
```
cd interview_bank
python app.py
```

### Step 4 — Open in browser
Go to: **http://127.0.0.1:5000**

---

## 📁 File Structure
```
interview_bank/
├── app.py              ← Python backend (Flask)
├── questions.json      ← Your questions data (auto-created)
├── requirements.txt    ← Dependencies
└── templates/
    └── index.html      ← Frontend (HTML + CSS + JS)
```

---

## 💡 Tips
- Your data is saved in `questions.json` — back it up anytime
- The app works 100% offline on your laptop
- To reset sample data, delete `questions.json` and restart
