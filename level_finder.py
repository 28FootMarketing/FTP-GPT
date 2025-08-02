#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import requests

def main():
    st.title("🏀 Level Finder GPT")
    
    st.markdown("Enter your details below to get a realistic college level recommendation:")
    
    sport = st.selectbox(
        "Primary Sport", 
        ["Football", "Basketball", "Soccer", "Baseball", "Softball", "Track", "Wrestling", "Other"]
    )
    
    gpa = st.text_input("GPA (e.g., 3.5)")
    height = st.text_input("Height (e.g., 6'1\")")
    weight = st.text_input("Weight (e.g., 185 lbs)")
    stats = st.text_area("Sport-Specific Stats (e.g., 18 PPG, 7 RPG)")
    activity = st.text_area("Recruiting Activity (e.g., emailed 10 coaches, posted highlights on Twitter)")
    
    if st.button("Find My Level"):
        # Validate inputs
        if not all([sport, gpa, height, weight]):
            st.warning("Please fill in all required fields (Sport, GPA, Height, Weight)")
            return
        
        payload = {
            "sport": sport,
            "gpa": gpa,
            "height": height,
            "weight": weight,
            "stats": stats,
            "activity": activity
        }
        
        try:
            with st.spinner("Getting your recommendation..."):
                response = requests.post(
                    "https://n8n.srv931648.hstgr.cloud/webhook-test/level-finder", 
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                
            st.markdown("### 📊 GPT Recommendation")
            st.write(response.text)
            
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the server. Please check your internet connection.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Server error: {e}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** Make sure to replace the webhook URL with your actual endpoint.")

if __name__ == "__main__":
    main()
