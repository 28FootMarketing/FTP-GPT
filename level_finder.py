import streamlit as st
import requests

st.set_page_config(page_title="🏀 Level Finder GPT", layout="centered")
st.title("🏀 Level Finder GPT")
st.markdown("Enter your details below to get a realistic college level recommendation:")

# Updated and expanded Baseball and Softball stats
sport_data = {
    "Basketball": {
        "PG": ["PPG", "APG", "Steals", "FG%"],
        "SG": ["PPG", "3P%", "Steals", "FG%"],
        "SF": ["PPG", "RPG", "Steals", "Blocks"],
        "PF": ["PPG", "RPG", "Blocks", "FG%"],
        "C":  ["RPG", "Blocks", "FG%", "PPG"]
    },
    "Baseball": {
        "Pitcher": ["ERA", "Wins", "Losses", "Strikeouts", "Walks", "WHIP", "Innings Pitched", "Hits Allowed", "Runs Allowed"],
        "Catcher": ["Caught Stealing %", "Putouts", "Assists", "Errors", "Passed Balls"],
        "Infielder": ["Batting Average", "Home Runs", "RBIs", "Runs Scored", "Stolen Bases", "Fielding %", "Double Plays", "Assists"],
        "Outfielder": ["Batting Average", "Home Runs", "RBIs", "Runs Scored", "Stolen Bases", "Fielding %", "Assists"]
    },
    "Softball": {
        "Pitcher": ["ERA", "Wins", "Strikeouts", "Walks", "WHIP", "Innings Pitched", "Hits Allowed", "Runs Allowed", "Shutouts", "No-Hitters"],
        "Catcher": ["Caught Stealing %", "Putouts", "Errors", "Passed Balls"],
        "Infielder": ["Batting Average", "Home Runs", "RBIs", "Runs Scored", "Stolen Bases", "Fielding %", "Double Plays", "Errors"],
        "Outfielder": ["Batting Average", "Home Runs", "RBIs", "Runs Scored", "Stolen Bases", "Fielding %", "Errors"]
    }
}

# UI selections
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
    submitted = st.form_submit_button("Find My Level")

# Submit
if submitted:
    with st.spinner("Analyzing your profile..."):
        stats_combined = ", ".join([f"{k}: {v}" for k, v in stat_inputs.items() if v])
        payload = {
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
            result = response.json()
            if result.get("success"):
                st.markdown("### ✅ GPT Recommendation")
                st.markdown(f"**🏅 Recommended Level:** {result.get('level')}")
                st.markdown(f"**✍️ Reason:** {result.get('reason')}")
                st.markdown("**🎯 Action Steps:**")
                for action in result.get("actions", []):
                    st.markdown(f"- {action}")
                st.markdown(f"**📋 Summary:** {result.get('summary')}")
            else:
                st.error("AI analysis failed.")
                st.text(f"Error: {result.get('error')}")
                st.text(f"Raw Output: {result.get('rawOutput')}")
        except Exception as e:
            st.error(f"Error occurred: {e}")
