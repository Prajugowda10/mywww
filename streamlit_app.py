import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(
    page_title="🌟 My Worth, My Wellness, My World",
    layout="wide",
    page_icon="🌈"
)

# --- App title ---
st.title("🌟 My Worth, My Wellness, My World")

st.markdown("""
Welcome to your personal transformation journey! 🚀  
Take this fun, interactive self-assessment to discover insights about your well-being.  
Let's build a world of wellness, together! 💫
""")

# --- Sidebar progress ---
st.sidebar.title("📊 Progress")
progress = st.sidebar.empty()

# --- Define sections ---
sections = {
    "💪 Body": [
        "How would you rate your current physical health (1-10)?",
        "How many hours of sleep do you get each night?",
        "How often do you exercise weekly?",
        "Rate your energy levels throughout the day (1-10)?",
    ],
    "🧠 Mindset": [
        "How optimistic are you overall (1-10)?",
        "How often do you experience negative self-talk (1-10)?",
        "Rate your confidence in achieving goals (1-10)?",
        "How easily do you adapt to change (1-10)?",
    ],
    "💓 Emotions": [
        "How well do you manage emotions (1-10)?",
        "How often do you feel stressed (1-10)?",
        "Rate your comfort expressing emotions (1-10)?",
        "How often do you practice self-compassion (1-10)?",
    ],
    "😄 Joy": [
        "How often do you feel joy (1-10)?",
        "How connected are you to your passions (1-10)?",
        "How often do you express gratitude (1-10)?",
        "Rate your overall contentment (1-10)?",
    ],
    "🤝 Relationships": [
        "How would you rate your relationships overall (1-10)?",
        "How supported do you feel by loved ones (1-10)?",
        "How well do you communicate your needs (1-10)?",
        "Rate your comfort in asking for help (1-10)?",
    ],
    "💰 Wealth": [
        "How satisfied are you with your financial situation (1-10)?",
        "Do you have clear financial goals (1-10)?",
        "Rate how well you manage finances (1-10)?",
        "How secure do you feel financially (1-10)?",
    ],
    "🎯 Purpose": [
        "How clear are you about your life's purpose (1-10)?",
        "How meaningful is your daily life (1-10)?",
        "How strong is your sense of fulfillment (1-10)?",
        "How inspired do you feel day-to-day (1-10)?",
    ],
    "🌍 Contribution": [
        "How often do you help or volunteer (1-10)?",
        "How much impact do you feel you make (1-10)?",
        "How connected are you to your community (1-10)?",
        "How satisfied are you with your contribution (1-10)?",
    ]
}

# --- Storage for scores ---
responses = {}
section_scores = {}

total_sections = len(sections)
counter = 0

# --- Collect data per section ---
for section, qs in sections.items():
    with st.expander(f"{section}"):
        st.markdown(f"### {section}")
        section_total = 0
        for q in qs:
            val = st.slider(q, 1, 10, 5)
            section_total += val
        avg = section_total / len(qs)
        section_scores[section] = avg
        counter += 1
        progress.progress(counter/total_sections)

# --- Display results button ---
if st.button("🚀 GO! Show My Results"):
    st.balloons()
    st.success("🎉 Assessment Completed! Here’s your personalized summary:")

    # --- Dataframe for radar chart ---
    categories = list(section_scores.keys())
    values = list(section_scores.values())

    df = pd.DataFrame(dict(
        section=categories,
        score=values
    ))

    # --- Radar chart using Plotly ---
    fig = px.line_polar(
        df,
        r='score',
        theta='section',
        line_close=True,
        range_r=[0,10],
        markers=True,
        template='plotly_dark',
        color_discrete_sequence=['#FF69B4']
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Display summary cards ---
    st.markdown("### 💡 **Your Well-Being Overview**")
    cols = st.columns(4)
    i = 0
    for sec, score in section_scores.items():
        if score < 5:
            color = "❌"
            msg = "Needs focus and care."
        elif score < 7:
            color = "⚠️"
            msg = "Doing okay, room for growth!"
        else:
            color = "✅"
            msg = "Great job! You're thriving."

        with cols[i % 4]:
            st.metric(
                label=f"{color} {sec}",
                value=f"{score:.1f} / 10",
                delta=msg
            )
        i += 1

    # --- Overall score ---
    overall = sum(section_scores.values()) / len(section_scores)
    st.markdown(f"""
        <div style='background-color: #4CAF50; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h2>🌟 Your Overall Well-Being Score: {overall:.2f} / 10</h2>
        </div>
    """, unsafe_allow_html=True)

    # --- Recommendations ---
    st.header("📌 Personalized Recommendations")

    for sec, score in section_scores.items():
        if score < 5:
            st.warning(f"**{sec}** → Consider focusing on this area. Explore support, learning, or coaching.")
        elif score < 7:
            st.info(f"**{sec}** → Good foundation! Keep building strength and exploring new ways to grow.")
        else:
            st.success(f"**{sec}** → Excellent! You’re thriving here. Keep shining! ✨")

else:
    st.info("⬆️ Complete the sliders above, then click **GO!** to see your personalized results.")
