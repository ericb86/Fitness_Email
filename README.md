# 🏋️‍♂️ Daily Fitness Email Automation

This Python script emails you a daily combination of:

- 🥣 A random **breakfast**, **lunch**, and **dinner** from your meal plan
- 💪 A workout tailored to the day of the week, blending gym and home recovery routines

The goal: make health and fitness effortless by removing decision fatigue — just open your inbox and follow the plan.

---

## 📦 Project Structure

```
daily_fitness_email/
├── fitness_emailer.py       # Main script
├── .env                     # Secure Gmail credentials (NOT committed)
├── .gitignore               # Hides sensitive files from GitHub
├── Meal Plan.csv            # Meals database (customizable)
├── Workout Circuits.csv     # Gym workout circuits
└── README.md                # Project overview
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/daily_fitness_email.git
cd daily_fitness_email
```

### 2. Install Dependencies

```bash
pip install pandas python-dotenv
```

### 3. Create a `.env` File

Inside the project root:

```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

> You’ll need to [enable 2-Step Verification](https://myaccount.google.com/security) on your Google account and [generate an App Password](https://myaccount.google.com/apppasswords).

### 4. Run the Script Manually

```bash
python fitness_emailer.py
```

---

## 🕖 Optional: Automate with Windows Task Scheduler

To run the script every morning at 7:00 AM:

1. Open **Task Scheduler**
2. Create a new task
3. Set **Trigger**: Daily at 7:00 AM
4. Set **Action**:
   - Program/script: `python.exe`
   - Add arguments: `"C:\path\to\daily_fitness_email\fitness_emailer.py"`
   - Start in: `C:\path\to\daily_fitness_email`
5. Check **“Wake the computer to run this task”**
6. Enter your **Windows username/password** so it can run unattended

---

## 🧠 Logic Summary

### 🥗 Meals
- Pulls from `Meal Plan.csv`
- Randomly selects one of each: breakfast, lunch, and dinner

### 🏃 Workouts
- Gym workouts on weekdays (Mon, Tue, Thu, Fri)
- At-home or recovery routines on Wed, Sat, Sun
- Pulls from `Workout Circuits.csv` + built-in light day logic

---

## ✅ Example Email Output

- Subject: `Your Fitness Plan for Wednesday`
- Content:
  - 🥣 Meals with macros and prep tips
  - 🏋️ Exercises with sets, reps, and video links

---

## 🔐 Security

Your `.env` file contains sensitive login info. Be sure:
- **Never commit it to GitHub**
- `.gitignore` includes `.env`
- You rotate your Gmail App Password if needed

---

## 🙋‍♂️ Made by Eric Barenholtz

Part of a personal project to automate healthy habits, reduce friction, and build muscle while reducing body fat.
