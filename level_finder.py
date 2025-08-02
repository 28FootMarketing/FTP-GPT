import streamlit as st
import requests

st.set_page_config(page_title="🏀 Level Finder GPT", layout="centered")
st.title("🏀 Level Finder GPT")
st.markdown("Enter your details below to get a realistic college level recommendation:")

# Full NFHS sport-to-position-to-stat map
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
    },
    "Soccer": {
        "GK": ["Saves", "Clean Sheets", "Goals Allowed"],
        "DEF": ["Tackles", "Clearances", "Interceptions"],
        "MID": ["Assists", "Pass Accuracy", "Tackles"],
        "FWD": ["Goals", "Shots on Target", "Assists"]
    },
    "Volleyball": {
        "Setter": ["Assists", "Digs", "Aces"],
        "Hitter": ["Kills", "Hitting %", "Blocks"],
        "Libero": ["Digs", "Serve Receive %", "Aces"]
    },
    "Track & Field": {
        "Sprinter": ["100m Time", "200m Time", "Relay Splits"],
        "Distance": ["800m Time", "1600m Time", "5K Time"],
        "Hurdles": ["110m Hurdles", "300m Hurdles"],
        "Jumps": ["High Jump", "Long Jump", "Triple Jump"],
        "Throws": ["Shot Put", "Discus", "Javelin"]
    },
    "Wrestling": {
        "Lightweight": ["Wins", "Pins", "Takedowns"],
        "Middleweight": ["Wins", "Pins", "Escapes"],
        "Heavyweight": ["Wins", "Pins", "Reversals"]
    },
    "Swimming & Diving": {
        "Swimmer": ["100m Freestyle", "200m IM", "Relay Splits"],
        "Diver": ["1m Score", "3m Score", "Form Score"]
    },
    "Tennis": {
        "Singles": ["Wins", "Aces", "Unforced Errors"],
        "Doubles": ["Wins", "Net Points", "Double Faults"]
    },
    "Golf": {
        "Player": ["Scoring Avg", "Fairways Hit", "Putts/Round"]
    },
    "Lacrosse": {
        "Attack": ["Goals", "Assists", "Shots on Goal"],
        "Midfield": ["Ground Balls", "Goals", "Clears"],
        "Defense": ["Caused Turnovers", "Ground Balls", "Saves"]
    },
    "Cheerleading": {
        "Base": ["Stunt Success", "Strength", "Stability"],
        "Flyer": ["Balance", "Flexibility", "Execution"],
        "Backspot": ["Support Rating", "Safety Awareness"]
    },
    "Esports": {
        "Player": ["Reaction Time", "KDA", "Win Rate"]
    },
    "Flag Football": {
        "QB": ["Passing Yards", "TDs", "Completions"],
        "WR": ["Receiving Yards", "Receptions", "TDs"],
        "DB": ["Interceptions", "Flags Pulled", "Passes Defended"]
    }
}

# UI
name = st.text_input("Athlete Name")
sport = st.selectbox("Sport", list(sport_data.keys()))
position = st.selectbox("Position", list(sport_data[sport].keys()))

st.markdown("**Enter your sport-specific stats:**")
stat_inputs = {}
for stat in sport_data[sport][position]:
    stat_inputs[stat] = st.text_input(stat)

# Other info
with st.form("level_form"):
    gpa = st.text_input("GPA")
    height = st.text_input("Height")
    weight = st.text_input("Weight")
    activity = st.text_area("Recruiting Activity")
    age = st.text_input("Age")
    experience = st.text_input("Experience")
    comment = st.text_input("Coach/Staff Comment")
    submitted = st.form_submit_button("Find My Level")

# Submission
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
                st.error("❌ Invalid JSON response")
                st.text(response.text)
                st.stop()
            if result.get("success"):
                st.markdown("### ✅ GPT Recommendation")
                st.markdown(f"**🏅 Level:** {result.get('level')}")
                st.markdown(f"**✍️ Reason:** {result.get('reason')}")
                st.markdown("**🎯 Action Steps:**")
                for action in result.get("actions", []):
                    st.markdown(f"- {action}")
                st.markdown(f"**📋 Summary:** {result.get('summary')}")
                st.markdown(f"**🗒️ Comment:** {comment if comment else 'N/A'}")
            else:
                st.error("AI analysis failed.")
                st.text(f"Error: {result.get('error')}")
        except Exception as e:
            st.error(f"Error occurred: {e}")
