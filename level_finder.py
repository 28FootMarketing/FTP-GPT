from datetime import datetime
import streamlit as st
import requests

st.set_page_config(page_title="Level Finder GPT", page_icon="🏅", layout="centered")

st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎯 Level Finder GPT</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find your most realistic college playing level — powered by AI</div>", unsafe_allow_html=True)

is_d1_check = st.toggle("🧠 Am I D1? Self-Check Mode")

nfhs_sports = [
    "Baseball", "Basketball", "Bowling", "Competitive Spirit", "Cross Country", "Field Hockey",
    "Football", "Golf", "Gymnastics", "Ice Hockey", "Lacrosse", "Rifle", "Soccer", "Softball",
    "Swim and Dive", "Tennis", "Track and Field", "Volleyball", "Water Polo", "Wrestling",
    "Girls Flag Football", "Esports"
]

with st.form("level_finder_form"):
    name = st.text_input("Student-Athlete Name")
    sport = st.selectbox("Sport", nfhs_sports)
    position = st.text_input("Primary Position")
    gpa = st.text_input("GPA", "3.8")
    age = st.text_input("Age", "17")
    height = st.text_input("Height (e.g., 6'2\")", "6'2")
    weight = st.text_input("Weight (e.g., 180 lbs)", "180 lbs")
    experience = st.text_input("Athletic Experience", "4 years varsity")
    stats = st.text_area("Key Sport Stats", "15 PPG, 8 RPG, 5 APG")
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
                "stats": stats,
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

                with st.expander("📋 Full Input & Evaluation Log"):
                    st.text(f"Name: {name}")
                    st.text(f"Sport: {sport}")
                    st.text(f"GPA: {gpa}")
                    st.text(f"Age: {age}")
                    st.text(f"Height: {height}")
                    st.text(f"Weight: {weight}")
                    st.text(f"Experience: {experience}")
                    st.text(f"Position: {position}")
                    st.text(f"Stats: {stats}")
                    st.text(f"Activity: {activity}")
                    st.text(f"Self-Check D1 Mode: {'Enabled' if is_d1_check else 'Disabled'}")

            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                st.text(result.get("rawOutput", "No raw output returned."))

        except Exception as e:
            st.error(f"Exception occurred: {str(e)}")
