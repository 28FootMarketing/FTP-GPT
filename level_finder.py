import streamlit as st
import requests

st.set_page_config(page_title='Level Finder GPT', page_icon='🏅', layout='centered')

st.markdown("""
    <style>
    .title { text-align: center; font-size: 36px; font-weight: bold; margin-bottom: 10px; }
    .subtitle { text-align: center; font-size: 18px; color: #555; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎯 Level Finder GPT</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find your most realistic college playing level — powered by AI</div>", unsafe_allow_html=True)

is_d1_check = st.toggle("🧠 Am I D1? Self-Check Mode")

# Combined structure for sports, positions, and stats (inline)
combined_data = {
  "Baseball": {
    "Pitcher": [
      "ERA",
      "Strikeouts",
      "Walks",
      "Innings Pitched"
    ],
    "Catcher": [
      "Caught Stealing %",
      "Fielding %",
      "Batting Average"
    ],
    "Infielder": [
      "Batting Average",
      "RBIs",
      "Fielding %"
    ],
    "Outfielder": [
      "Batting Average",
      "Runs",
      "Fielding %"
    ],
    "Designated Hitter": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Basketball": {
    "Point Guard": [
      "Points Per Game",
      "Assists",
      "Turnovers",
      "Steals"
    ],
    "Shooting Guard": [
      "Points Per Game",
      "3-Point %",
      "Rebounds"
    ],
    "Small Forward": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Power Forward": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Center": [
      "Points",
      "Blocks",
      "Rebounds"
    ]
  },
  "Bowling": {
    "Individual": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Competitive Spirit": {
    "Base": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Flyer": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Tumbler": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Cross Country": {
    "Runner": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Field Hockey": {
    "Forward": [
      "Goals",
      "Assists",
      "Shots on Goal"
    ],
    "Midfield": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Defense": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Goalkeeper": [
      "Saves",
      "Goals Allowed",
      "Save %"
    ]
  },
  "Football": {
    "Quarterback": [
      "Passing Yards",
      "Touchdowns",
      "Interceptions",
      "Completion %"
    ],
    "Running Back": [
      "Rushing Yards",
      "Touchdowns",
      "Yards Per Carry"
    ],
    "Wide Receiver": [
      "Receiving Yards",
      "Touchdowns",
      "Receptions"
    ],
    "Linebacker": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Defensive Back": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Offensive Line": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Kicker": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Golf": {
    "Individual": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Gymnastics": {
    "Vault": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Bars": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Beam": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Floor": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Ice Hockey": {
    "Forward": [
      "Goals",
      "Assists",
      "Shots on Goal"
    ],
    "Defense": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Goalie": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Lacrosse": {
    "Attack": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Midfield": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Defense": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Goalie": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Rifle": {
    "Air Rifle": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Smallbore": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Soccer": {
    "Forward": [
      "Goals",
      "Assists",
      "Shots on Goal"
    ],
    "Midfielder": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Defender": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Goalkeeper": [
      "Saves",
      "Goals Allowed",
      "Save %"
    ]
  },
  "Softball": {
    "Pitcher": [
      "ERA",
      "Strikeouts",
      "Walks",
      "Innings Pitched"
    ],
    "Catcher": [
      "Caught Stealing %",
      "Fielding %",
      "Batting Average"
    ],
    "Infielder": [
      "Batting Average",
      "RBIs",
      "Fielding %"
    ],
    "Outfielder": [
      "Batting Average",
      "Runs",
      "Fielding %"
    ]
  },
  "Swim and Dive": {
    "Freestyle": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Backstroke": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Breaststroke": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Butterfly": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Diver": [
      "Average Score",
      "Degree of Difficulty"
    ]
  },
  "Tennis": {
    "Singles": [
      "Win/Loss Record",
      "Matches Played"
    ],
    "Doubles": [
      "Team Record",
      "Net Play %"
    ]
  },
  "Track and Field": {
    "Sprinter": [
      "100m Time",
      "200m Time",
      "400m Time"
    ],
    "Distance Runner": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Thrower": [
      "Shot Put Distance",
      "Discus Distance"
    ],
    "Jumper": [
      "High Jump",
      "Long Jump",
      "Triple Jump"
    ],
    "Hurdler": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Volleyball": {
    "Setter": [
      "Assists",
      "Service Aces",
      "Blocks"
    ],
    "Libero": [
      "Digs",
      "Serve Receive %",
      "Passing"
    ],
    "Middle Blocker": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Outside Hitter": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Right Side": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Water Polo": {
    "Attacker": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Defender": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Goalkeeper": [
      "Saves",
      "Goals Allowed",
      "Save %"
    ],
    "Utility": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Wrestling": {
    "Lightweight": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Middleweight": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Heavyweight": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Girls Flag Football": {
    "Quarterback": [
      "Passing Yards",
      "Touchdowns",
      "Interceptions",
      "Completion %"
    ],
    "Running Back": [
      "Rushing Yards",
      "Touchdowns",
      "Yards Per Carry"
    ],
    "Receiver": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Safety": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ],
    "Rusher": [
      "Stat 1",
      "Stat 2",
      "Stat 3"
    ]
  },
  "Esports": {
    "Player": [
      "Kills",
      "Deaths",
      "Assists",
      "Rank"
    ]
  }
}

sports = list(combined_data.keys())
sport = st.selectbox("Sport", sports)
positions = list(combined_data[sport].keys())
position = st.selectbox("Primary Position", positions)

with st.form("level_finder_form"):
    name = st.text_input("Student-Athlete Name")
    gpa = st.text_input("GPA", "3.8")
    age = st.text_input("Age", "17")
    height = st.text_input("Height (e.g., 6'2\")", "6'2")
    weight = st.text_input("Weight (e.g., 180 lbs)", "180 lbs")
    experience = st.text_input("Athletic Experience", "4 years varsity")

    st.markdown("**📊 Enter Stat Details Below:**")
    stat_inputs = {}
    for stat_label in combined_data[sport][position]:
        stat_inputs[stat_label] = st.text_input(stat_label)

    activity = st.text_input("Recruiting Activity", "Daily training, highlight video posted, contacted 5 coaches")
    submit = st.form_submit_button("🎓 Evaluate My Level")

if submit:
    with st.spinner("Evaluating your recruiting level..."):
        try:
            payload = {
                "name": name,
                "sport": sport,
                "gpa": gpa,
                "age": age,
                "height": height,
                "weight": weight,
                "experience": experience,
                "position": position,
                "stats": stat_inputs,
                "activity": activity,
                "d1_check": is_d1_check
            }

            response = requests.post("https://ftp-gpt.streamlit.app/api/level-finder", json=payload)
            result = response.json()

            if result.get("success"):
                st.success("✅ Evaluation Complete")
                st.markdown("### 🧾 Recommendation Summary")
                st.markdown(f"**🎓 Recommended Level:** {result['level']}")
                st.markdown(f"**📌 Reason:** {result['reason']}")
                st.markdown("**📈 Action Steps:**")
                for step in result.get("actions", []):
                    st.markdown(f"- {step}")
                st.markdown(f"**🧠 Summary:** {result['summary']}")
                st.markdown(f"**📅 Timestamp:** {result['timestamp']}")

                with st.expander("📋 Full Input Log"):
                    st.text(f"Name: {name}")
                    st.text(f"Sport: {sport}")
                    st.text(f"Position: {position}")
                    st.text(f"GPA: {gpa}")
                    st.text(f"Age: {age}")
                    st.text(f"Height: {height}")
                    st.text(f"Weight: {weight}")
                    st.text(f"Experience: {experience}")
                    for k, v in stat_inputs.items():
                        st.text(f"{k}: {v}")
                    st.text(f"Activity: {activity}")
                    st.text(f"D1 Mode: {'Yes' if is_d1_check else 'No'}")
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                st.text(result.get("rawOutput", "No raw output returned."))

        except Exception as e:
            st.error(f"Exception occurred: {str(e)}")
