
import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Level Finder GPT", page_icon="🏆", layout="centered")

st.markdown("<h1 style='text-align: center;'>🏆 Level Finder GPT</h1>", unsafe_allow_html=True)
st.markdown("Use this form to evaluate your current recruiting level based on your profile. Fill in all fields accurately.")

# Full NFHS sports list
sports = [
    "Baseball", "Softball", "Basketball", "Football", "Soccer", "Volleyball", "Wrestling",
    "Track and Field", "Cross Country", "Swimming and Diving", "Tennis", "Golf",
    "Lacrosse", "Field Hockey", "Gymnastics", "Ice Hockey", "Cheerleading", "Dance",
    "Bowling", "Esports", "Badminton", "Water Polo", "Rugby", "Weightlifting", "Skiing", "Snowboarding"
]

sport = st.selectbox("Sport", sports)

positions_map = {
    "Baseball": ["Pitcher", "Catcher", "Infield", "Outfield", "Utility"],
    "Softball": ["Pitcher", "Catcher", "Infield", "Outfield", "Utility"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Football": ["Quarterback", "Running Back", "Wide Receiver", "Tight End", "Linebacker", "Defensive Back", "Offensive Lineman", "Defensive Lineman", "Kicker"],
    "Soccer": ["Goalkeeper", "Defender", "Midfielder", "Forward"],
    "Volleyball": ["Setter", "Outside Hitter", "Middle Blocker", "Libero", "Opposite Hitter"],
    "Wrestling": ["Lightweight", "Middleweight", "Heavyweight"],
    "Esports": ["FPS", "MOBA", "Sports Sim", "Fighting"],
    # Add remaining sports and default roles
}

position = st.selectbox("Position", positions_map.get(sport, ["General"]))

stat_categories = {
    "Baseball": ["ERA", "Batting Avg", "Home Runs", "RBIs", "Fielding %"],
    "Softball": ["ERA", "Batting Avg", "Home Runs", "RBIs", "Fielding %"],
    "Basketball": ["Points Per Game", "Rebounds", "Assists", "Steals", "Blocks"],
    "Football": ["Passing Yards", "Rushing Yards", "Tackles", "Sacks", "Interceptions"],
    "Soccer": ["Goals", "Assists", "Saves", "Tackles", "Pass Completion %"],
    "Volleyball": ["Kills", "Blocks", "Aces", "Digs", "Assists"],
    "Wrestling": ["Win %", "Pins", "Takedowns", "Escapes"],
    "Esports": ["K/D Ratio", "Win %", "Reaction Time", "Game Rank"],
    # Expand for all NFHS sports
}

# Dynamic stat fields
st.subheader("Enter Your Key Stats")
stats = {}
for category in stat_categories.get(sport, ["Custom Stat 1", "Custom Stat 2"]):
    stats[category] = st.text_input(f"{category}")

st.subheader("Academic and Personal Info")
gpa = st.text_input("GPA", "3.5")
age = st.text_input("Age", "17")
height = st.text_input("Height", "6'2"")
weight = st.text_input("Weight", "180 lbs")
experience = st.text_input("Experience (e.g. 3 years varsity)", "")
activity = st.text_input("Training/Playing Activity", "3 games per week, daily practice")

if st.button("Analyze My Level"):
    with st.spinner("Analyzing..."):
        payload = {
            "sport": sport,
            "position": position,
            "gpa": gpa,
            "age": age,
            "height": height,
            "weight": weight,
            "experience": experience,
            "activity": activity,
            "stats": ", ".join([f"{k}: {v}" for k, v in stats.items()])
        }

        try:
            res = requests.post("http://localhost:5678/webhook/level-finder", json=payload)
            res.raise_for_status()
            result = res.json()
            st.success("Analysis complete!")

            st.subheader("📊 Recommended Level")
            st.markdown(f"**Level:** {result['level']}")
            st.markdown(f"**Reason:** {result['reason']}")
            st.markdown("**Action Steps:**")
            for step in result["actions"]:
                st.markdown(f"- {step}")
            st.markdown(f"**Summary:** {result['summary']}")
        except Exception as e:
            st.error(f"Error occurred: {e}")
