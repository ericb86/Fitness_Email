
import os
import random
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv('GMAIL_USER')
EMAIL_PASS = os.getenv('GMAIL_APP_PASSWORD')

# Load meal data
meal_df = pd.read_csv("meal_plan.csv")
breakfasts = meal_df[meal_df['Meal Type'].str.lower() == 'breakfast']
lunches = meal_df[meal_df['Meal Type'].str.lower() == 'lunch']
dinners = meal_df[meal_df['Meal Type'].str.lower() == 'dinner']

# Load workout data
workout_df = pd.read_csv("workout_circuits.csv")

# Create custom home recovery workouts
home_workouts = {
    "Wednesday – Active Recovery + Core": [
        "Bird-Dog (3x12/side)",
        "Dead Bug (3x10)",
        "Plank (3x30s)",
        "Wall Angels (3x15)"
    ],
    "Saturday – Mobility + Cardio": [
        "Jump Rope or March in Place (5 min)",
        "Yoga Flow (10 min)",
        "Glute Bridges (3x12)",
        "Foam Rolling"
    ],
    "Sunday – Stretch & Reset": [
        "Hip Flexor Stretch",
        "Hamstring Stretch",
        "Child’s Pose",
        "Deep Breathing"
    ]
}

# Determine today's day name
today = datetime.now().strftime("%A")

# Meal selection
breakfast = breakfasts.sample(1).iloc[0]
lunch = lunches.sample(1).iloc[0]
dinner = dinners.sample(1).iloc[0]

# Workout selection
if today in ["Wednesday", "Saturday", "Sunday"]:
    workout_title = today + " – Home Day"
    exercises = home_workouts.get(workout_title, home_workouts[today + " – Stretch & Reset"])
    workout_html = f"<h3>{workout_title}</h3><ul>" + ''.join([f"<li>{ex}</li>" for ex in exercises]) + "</ul>"
else:
    matching_day = workout_df[workout_df['Day'].str.contains(today, case=False, na=False)]
    if not matching_day.empty:
        circuits = matching_day['Circuit'].unique()
        chosen_circuit = random.choice(circuits)
        filtered = matching_day[matching_day['Circuit'] == chosen_circuit]
        workout_html = f"<h3>{today} – {chosen_circuit}</h3><ul>"
        for _, row in filtered.iterrows():
            video = row['Video Link'].split('"')[1] if 'HYPERLINK' in row['Video Link'] else row['Video Link']
            workout_html += f"<li>{row['Exercise']} – {row['Sets/Reps']} – <a href='{video}'>Video</a></li>"
        workout_html += "</ul>"
    else:
        workout_html = "<p>No gym workout found for today.</p>"

# Format meals into HTML
def meal_html(meal, label):
    return f"""
    <h3>{label}</h3>
    <p><strong>{meal['Meal Name']}</strong><br>
    Protein: {meal['Protein (g)']}g, Carbs: {meal['Carbs (g)']}g, Fats: {meal['Fats (g)']}g<br>
    Fiber: {meal['Fiber (g)']}g, Calories: {meal['Calories']}<br>
    Carb Type: {meal['Carb Type']}, Veg: {meal['Fiber First Veg']}<br>
    Notes: {meal['Prep Notes']}</p>
    """

meal_section = meal_html(breakfast, "Breakfast") + meal_html(lunch, "Lunch") + meal_html(dinner, "Dinner")

# Build email
msg = MIMEMultipart("alternative")
msg["Subject"] = f"Your Fitness Plan for {today}"
msg["From"] = "Eric’s Fitness Bot"
msg["To"] = EMAIL_USER

html = f"""
<html>
  <body>
    <h2>👋 Good Morning, Eric!</h2>
    {meal_section}
    <hr>
    {workout_html}
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

# Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())
    print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Email failed to send:", str(e))
