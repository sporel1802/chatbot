import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Personal Fitness Advisor", page_icon="💪")

st.title("💪 AI Personal Fitness Advisor")
st.write("Enter your details below to get personalized fitness advice.")

# -----------------------------
# User Inputs
# -----------------------------
age = st.number_input("Age", 10, 100)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
height = st.number_input("Height (in cm)", min_value=0.0)
weight = st.number_input("Weight (in kg)", min_value=0.0)
sleep = st.number_input("Average Sleeping Hours per Day", 0, 24)
exercise = st.selectbox(
    "Exercise Frequency",
    ["None", "1-2 days/week", "3-5 days/week", "Daily"]
)
goal = st.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Muscle Gain", "Stay Fit", "Improve Stamina"]
)

# -----------------------------
# BMI Calculation
# -----------------------------
bmi = None

if height > 0 and weight > 0:
    bmi = weight / ((height / 100) ** 2)
    st.write(f"### 📊 Your BMI: {bmi:.2f}")

# -----------------------------
# Generate AI Advice
# -----------------------------
if st.button("Get Fitness Advice"):

    if bmi is None:
        st.error("Please enter valid height and weight.")
    else:
        prompt = f"""
        User Details:
        Age: {age}
        Gender: {gender}
        Height: {height} cm
        Weight: {weight} kg
        BMI: {bmi:.2f}
        Sleeping Hours: {sleep}
        Exercise Frequency: {exercise}
        Fitness Goal: {goal}

        Based on the above details:
        1. Analyze health condition.
        2. Suggest improvements.
        3. Provide diet recommendations.
        4. Suggest workout plan.
        5. Suggest sleep improvements.
        6. Provide motivational advice.
        """

        with st.spinner("Generating your personalized fitness plan..."):

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional certified fitness trainer. Give structured, safe and practical advice."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                advice = response.choices[0].message.content

                st.success("Here is your AI-generated fitness plan:")
                st.markdown(advice)

            except Exception as e:
                st.error(f"Error: {e}")