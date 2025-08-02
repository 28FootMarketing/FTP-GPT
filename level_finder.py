import streamlit as st
import requests

st.set_page_config(page_title="Level Finder GPT", layout="centered")
st.title("Level Finder GPT")
st.markdown("Enter your details below to get a realistic college level recommendation:")

# Simplified sample of all NFHS-recognized sports (expandable)
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
    "Soccer": {
        "GK": ["Saves", "Clean Sheets", "Goals Allowed"],
        "DEF": ["Tackles", "Clearances", "Interceptions"],
        "MID": ["Assists", "Pass Accuracy", "Tackles"],
        "FWD": ["Goals", "Shots on Target", "Assists"]
    },
    "Baseball": {
        "P": ["ERA", "Strikeouts", "WHIP", "Walks"],
        "C": ["Caught Stealing %", "Putouts", "Fielding %"],
        "INF": ["Batting Average", "RBIs", "Double Plays"],
        "OF": ["Fielding %", "Assists", "Errors"]
    },
    "Softball": {
        "P": ["ERA", "Strikeouts", "Walks"],
        "C": ["Caught Stealing %", "Putouts"],
        "INF": ["Batting Avg", "RBIs", "Errors"],
        "OF": ["Fielding %", "Assists"]
    },
    "Track & Field": {
        "Sprinter": ["100m Time", "200m Time", "Relay Splits"],
        "Distance": ["800m Time", "1600m Time", "5K Time"],
        "Hurdles": ["110m Hurdles", "300m Hurdles"],
        "Jumps": ["High Jump", "Long Jump", "Triple Jump"],
        "Throws": ["Shot Put", "Discus", "Javelin"]
    },
    "Volleyball": {
        "Setter": ["Assists", "Digs", "Aces"],
        "Hitter": ["Kills", "Hitting %", "Blocks"],
        "Libero": ["Digs", "Serve Receive %", "Aces"]
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
