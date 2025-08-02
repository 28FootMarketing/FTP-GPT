import streamlit as st
import requests

st.set_page_config(page_title="🏀 Level Finder GPT", layout="centered")

st.title("🏀 Level Finder GPT")
st.markdown("Enter your details below to get a realistic college level recommendation:")

# Form inputs
with st.form("level_form"):
    sport = st.selectbox("Primary Sport", ["Football", "Basketball", "Soccer", "Baseball", "Softball", "Track", "Wrestling", "Other"])
    gpa = st.text_input("GPA (e.g., 3.5)")
    height = st.text_input("Height (e.g., 6'1\")")
    weight = st.text_input("Weight (e.g., 185 lbs)")
    stats = st.text_area("Sport-Specific Stats (e.g., 18 PPG, 7 RPG)")
    activity = st.text_area("Recruiting Activity (e.g., emailed 10 coaches, posted highlights on Twitter)")
    age = st.text_input("Age (e.g., 17)")
    experience = st.text_input("Experience (e.g., 4 years varsity)")
    submitted = st.form_submit_button("Find My Level")

# Submit and display recommendation
if submitted:
    with st.spinner("Analyzing your profile..."):
        payload = {
            "sport": sport,
            "gpa": gpa,
            "height": height,
            "weight": weight,
            "stats": stats,
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
