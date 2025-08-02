import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="🏆 Level Finder GPT", layout="centered")

# Header
st.markdown("""
    <h1 style="text-align:center; color:#1E3A8A;">🏆 Level Finder GPT</h1>
    <h4 style="text-align:center; color:#3B82F6;">
        Discover your most realistic college playing level based on performance, academics, and more.
    </h4>
    <hr style="border-top: 2px solid #3B82F6;">
""", unsafe_allow_html=True)

# Sport, Position, Stat Data
sport_data = {
    "Basketball": {
        "PG": ["PPG", "APG", "Steals", "FG%"],
        "SG": ["PPG", "3P%", "Steals", "FG%"],
        "SF": ["PPG", "RPG", "Steals", "Blocks"],
        "PF": ["PPG", "RPG", "Blocks", "FG%"],
        "C":  ["RPG", "Blocks", "FG%", "PPG"]
    },
    "Football": {
        "QB": ["Passing Yards", "TDs", "Completions", "INTs"],
        "RB": ["Rushing Yards", "TDs", "Carries", "Yards/Carry"],
        "WR": ["Receiving Yards", "TDs", "Receptions", "Yards/Catch"],
        "LB": ["Tackles", "Sacks", "INTs", "Forced Fumbles"],
        "DB": ["Tackles", "INTs", "Passes Defended", "TDs"],
        "OL": ["Pancake Blocks", "Penalties", "Sacks Allowed"],
        "DL": ["Tackles", "Sacks", "Pressures", "TFLs"]
    },
    "Baseball": {
        "Pitcher": ["ERA", "Wins", "Strikeouts", "WHIP", "Innings Pitched"],
        "Catcher": ["Caught Stealing %", "Putouts", "Errors", "Passed Balls"],
        "Infielder": ["Batting Average", "RBIs", "Fielding %", "Double Plays"],
        "Outfielder": ["Batting Average", "Home Runs", "Fielding %", "Assists"]
    },
    "Softball": {
        "Pitcher": ["ERA", "Wins", "Strikeouts", "WHIP", "Shutouts", "No-Hitters"],
        "Catcher": ["Caught Stealing %", "Putouts", "Errors", "Passed Balls"],
        "Infielder": ["Batting Average", "RBIs", "Stolen Bases", "Fielding %"],
        "Outfielder": ["Batting Average", "Home Runs", "Fielding %", "Errors"]
    }
}

# Input: Athlete Info
st.markdown("### 🧍 Athlete Information")
name = st.text_input("Athlete Name")
col1, col2, col3 = st.columns(3)
with col1:
    height = st.text_input("Height", "6'2"")
with col2:
    weight = st.text_input("Weight", "180 lbs")
with col3:
    age = st.text_input("Age", "17")

gpa = st.text_input("GPA", "3.8", help="Your current unweighted GPA on a 4.0 scale")
experience = st.text_input("Experience", help="How many years have you played?")
activity = st.text_area("Recruiting Activity", help="Any outreach to coaches, highlight videos, camps, etc.")
comment = st.text_input("Coach/Staff Comment")

st.markdown("---")
st.markdown("### 🏅 Sport & Stats")

# Sport + Position
sport = st.selectbox("Choose your sport", list(sport_data.keys()))
position = st.selectbox("Choose your position", list(sport_data[sport].keys()))
st.markdown("#### 🔢 Enter your sport-specific stats:")
stat_inputs = {}
for stat in sport_data[sport][position]:
    stat_inputs[stat] = st.text_input(stat)

# Submit
if st.button("🔍 Find My Level"):
    with st.spinner("Analyzing your profile..."):
        stats_combined = ", ".join([f"{k}: {v}" for k, v in stat_inputs.items() if v])
        payload = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "sport": sport,
            "position": position,
            "gpa": gpa,
            "height": height,
            "weight": weight,
            "age": age,
            "experience": experience,
            "stats": stats_combined,
            "activity": activity
        }
        try:
            response = requests.post("https://your-vps-url.com/webhook/level-finder", json=payload)
            try:
                result = response.json()
            except ValueError:
                st.error("❌ Invalid JSON response from server.")
                st.text(response.text)
                st.stop()

            if result.get("success"):
                st.markdown(f"""
                    <div style="background-color:#F0F9FF;padding:15px;border-radius:10px;border-left:5px solid #3B82F6;">
                        <h4>🎯 <b>Recommended Level:</b> {result.get('level')}</h4>
                        <p><b>Reason:</b> {result.get('reason')}</p>
                        <p><b>Summary:</b> {result.get('summary')}</p>
                        <p><b>Action Steps:</b></p>
                        <ul>
                            {''.join([f"<li>{a}</li>" for a in result.get("actions", [])])}
                        </ul>
                        <p><b>Coach Comment:</b> {comment if comment else "N/A"}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("AI recommendation failed.")
                st.text(f"Error: {result.get('error')}")
        except Exception as e:
            st.error(f"Error occurred: {e}")

# Footer
st.markdown("""
    <hr>
    <p style="text-align:center;font-size:0.9em;color:#9CA3AF;">
        Powered by <b>Facilitate The Process</b> | Built with Streamlit + GPT + Ollama
    </p>
""", unsafe_allow_html=True)
