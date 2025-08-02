from datetime import datetime
import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Level Finder GPT", page_icon="🏅", layout="centered")
st.markdown("<h2 style='text-align: center;'>🎯 Level Finder GPT</h2>", unsafe_allow_html=True)

# Toggle for "Am I D1?" Self-Check Mode
is_d1_check = st.toggle("🧠 Am I D1? Self-Check Mode")

# Input fields
with st.form("level_finder_form"):
    name = st.text_input("Name")
    sport = st.selectbox("Sport", ["Basketball", "Football", "Soccer", "Baseball", "Softball", "Track and Field"])
    gpa = st.text_input("GPA", "3.8")
    age = st.text_input("Age", "17")
    height = st.text_input("Height", "6'2\"")
    weight = st.text_input("Weight", "180 lbs")
    experience = st.text_input("Experience", "4 years varsity")
    position = st.text_input("Position", "")
    stats = st.text_area("Stats (Sport-specific)", "15 PPG, 8 RPG, 5 APG")
    activity = st.text_input("Activity Level", "Daily training, 3 games/week")
    submit = st.form_submit_button("Evaluate Level")

if submit:
    with st.spinner("Evaluating..."):
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
                st.success("Evaluation Complete")
                st.markdown(f"### 🧾 Recommendation Summary")
                st.markdown(f"**Recommended Level:** {result['level']}")
                st.markdown(f"**Reason:** {result['reason']}")
                st.markdown("**Action Steps:**")
                for step in result.get("actions", []):
                    st.markdown(f"- {step}")
                st.markdown(f"**Summary:** {result['summary']}")
                st.markdown(f"**Timestamp:** {result['timestamp']}")

                with st.expander("📌 Full Input + Evaluation Log"):
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
                st.error(f"Error: {result.get('error', 'Unknown error')}")
                st.text(result.get("rawOutput", "No raw output returned."))

        except Exception as e:
            st.error(f"Exception occurred: {str(e)}")
