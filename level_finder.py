import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Level Finder GPT", layout="centered")
st.title(" Level Finder GPT")
st.markdown("Enter your details below to get a realistic college level recommendation:")

# Placeholder sport data to avoid truncation
sport_data = {
    "Basketball": {"PG": ["PPG", "APG", "Steals"]},
    "Football": {"QB": ["Passing Yards", "TDs"]},
    "Baseball": {"Pitcher": ["ERA", "Strikeouts"]},
    "Softball": {"Pitcher": ["ERA", "Strikeouts"]},
    "Track & Field": {"Sprinter": ["100m Time"]},
    "Soccer": {"GK": ["Saves"]},
    "Volleyball": {"Setter": ["Assists"]},
    "Wrestling": {"Heavyweight": ["Wins"]},
    "Swimming & Diving": {"Swimmer": ["100m Freestyle"]},
    "Tennis": {"Singles": ["Wins"]},
    "Golf": {"Player": ["Scoring Avg"]},
    "Lacrosse": {"Attack": ["Goals"]},
    "Cheerleading": {"Base": ["Stunt Success"]},
    "Esports": {"Player": ["KDA"]},
    "Flag Football": {"QB": ["Passing Yards"]}
}

# UI selections
name = st.text_input("Athlete Name")
sport = st.selectbox("Select Your Sport", list(sport_data.keys()))
position = st.selectbox("Select Your Position", list(sport_data[sport].keys()))
stat_inputs = {}
st.markdown("**Enter your sport-specific stats:**")
for stat in sport_data[sport][position]:
    stat_inputs[stat] = st.text_input(stat)

# Additional inputs
with st.form("level_form"):
    gpa = st.text_input("GPA (e.g., 3.5)")
    height = st.text_input("Height (e.g., 6'1\")")
    weight = st.text_input("Weight (e.g., 185 lbs)")
    activity = st.text_area("Recruiting Activity (e.g., tournaments, showcases)")
    age = st.text_input("Age (e.g., 17)")
    experience = st.text_input("Experience (e.g., 4 years varsity)")
    comment = st.text_input("Coach/Staff Comment (optional)")
    submitted = st.form_submit_button("Find My Level")

# Submit
if submitted:
    with st.spinner("Analyzing your profile..."):
        stats_combined = ", ".join([f"{k}: {v}" for k, v in stat_inputs.items() if v])
        payload = {
            "name": name,
            "sport": sport,
            "position": position,
            "gpa": gpa,
            "height": height,
            "weight": weight,
            "stats": stats_combined,
            "activity": activity,
            "age": age,
            "experience": experience
        }
        try:
            response = requests.post("https://your-vps-url.com/webhook/level-finder", json=payload)

            try:
                result = response.json()
            except ValueError:
                st.error("❌ Response is not valid JSON. Here is the raw output:")
                st.text(response.text)
                st.stop()

            if result.get("success"):
                st.markdown("### ✅ GPT Recommendation")
                st.markdown(f"**🏅 Recommended Level:** {result.get('level')}")
                st.markdown(f"**✍️ Reason:** {result.get('reason')}")
                st.markdown("**🎯 Action Steps:**")
                for action in result.get("actions", []):
                    st.markdown(f"- {action}")
                st.markdown(f"**📋 Summary:** {result.get('summary')}")
                st.markdown(f"**🗒️ Comment:** {comment if comment else 'N/A'}")

            else:
                st.error("AI analysis failed.")
                st.text(f"Error: {result.get('error')}")
                st.text(f"Raw Output: {result.get('rawOutput')}")

        except Exception as e:
            st.error(f"Error occurred: {e}")
