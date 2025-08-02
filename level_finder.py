import streamlit as st
import requests

st.set_page_config(page_title=" Level Finder GPT", layout="centered")
st.title(" Level Finder GPT")
st.markdown("Enter your details below to get a realistic college level recommendation:")

# Expanded sport → positions → stats dictionary
sport_data = {
    "Basketball": {
        "positions": ["PG", "SG", "SF", "PF", "C"],
        "stats": ["PPG", "RPG", "APG", "FG%", "Steals", "Blocks"]
    },
    "Football": {
        "positions": ["QB", "RB", "WR", "LB", "DB", "OL", "DL"],
        "stats": ["Passing Yards", "Rushing Yards", "Receiving Yards", "Tackles", "Sacks", "Interceptions"]
    },
    "Soccer": {
        "positions": ["GK", "DEF", "MID", "FWD"],
        "stats": ["Goals", "Assists", "Clean Sheets", "Saves", "Tackles", "Pass Accuracy"]
    },
    "Baseball": {
        "positions": ["P", "C", "1B", "2B", "3B", "SS", "OF"],
        "stats": ["Batting Average", "Home Runs", "RBIs", "Stolen Bases", "ERA", "Strikeouts"]
    },
    "Softball": {
        "positions": ["P", "C", "1B", "2B", "3B", "SS", "OF"],
        "stats": ["Batting Average", "RBIs", "Stolen Bases", "ERA", "Strikeouts", "On-base %"]
    },
    "Volleyball": {
        "positions": ["Setter", "Outside Hitter", "Middle Blocker", "Libero", "Opposite"],
        "stats": ["Kills", "Assists", "Blocks", "Digs", "Aces", "Hitting %"]
    },
    "Track & Field": {
        "positions": ["Sprinter", "Distance", "Hurdles", "Jumps", "Throws"],
        "stats": ["100m Time", "Mile Time", "Hurdles Time", "Jump Distance", "Throw Distance"]
    },
    "Wrestling": {
        "positions": ["Lightweight", "Middleweight", "Heavyweight"],
        "stats": ["Wins", "Pins", "Takedowns", "Escape Points", "Matches"]
    },
    "Cheerleading": {
        "positions": ["Base", "Flyer", "Backspot"],
        "stats": ["Stunt Difficulty", "Routine Execution", "Jumps Score", "Tumbling Score"]
    }
}

# Step 2: Form UI
with st.form("level_form"):
    sport = st.selectbox("Primary Sport", list(sport_data.keys()))
    position = st.selectbox("Primary Position", sport_data[sport]["positions"])
    stat_inputs = {}
    st.markdown("**Enter your sport-specific stats:**")
    for stat in sport_data[sport]["stats"]:
        value = st.text_input(f"{stat}")
        stat_inputs[stat] = value

    # General info
    gpa = st.text_input("GPA (e.g., 3.5)")
    height = st.text_input("Height (e.g., 6'1\")")
    weight = st.text_input("Weight (e.g., 185 lbs)")
    activity = st.text_area("Recruiting Activity (e.g., emailed 10 coaches, posted highlights on Twitter)")
    age = st.text_input("Age (e.g., 17)")
    experience = st.text_input("Experience (e.g., 4 years varsity)")

    submitted = st.form_submit_button("Find My Level")

# Step 3: Submit
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
