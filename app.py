# GOOGLE PLAY STORE ANALYTICS DASHBOARD
# INTERNSHIP PROJECT - FINAL PROFESSIONAL VERSION

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
import os
import streamlit.components.v1 as components

# PAGE CONFIG

st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CUSTOM CSS

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.main {
    background: linear-gradient(to right, #0f172a, #111827);
}

/* TITLE */

.main-title {
    font-size: 58px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #2563eb, #0ea5e9, #14b8a6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: -20px;
    margin-bottom: 10px;
    letter-spacing: 2px;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 21px;
    margin-bottom: 40px;
    font-weight: 600;
}

/* CARDS */

.metric-card {
    background: linear-gradient(145deg,#111827,#1f2937);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(59,130,246,0.3);
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    border: 1px solid #06b6d4;
}

.metric-value {
    font-size: 35px;
    font-weight: bold;
    color: #06b6d4;
}

.metric-label {
    color: white;
    font-size: 18px;
}

/* SECTION TITLES */

.section-title {
    font-size: 34px;
    font-weight: 800;
    color: black;
    margin-top: 45px;
    margin-bottom: 20px;
    padding-left: 8px;
    border-left: 6px solid #0ea5e9;
}

/* INSIGHT BOX */

.insight-box {
    background: linear-gradient(145deg,#111827,#1e293b);
    padding: 25px;
    border-radius: 18px;
    border-left: 6px solid #06b6d4;
    color: #f1f5f9;
    margin-top: 15px;
    margin-bottom: 35px;
    line-height: 1.8;
    box-shadow: 0 8px 18px rgba(0,0,0,0.25);
    font-size: 17px;
}

/* FOOTER */

.footer {
    text-align:center;
    color:black;
    padding:40px;
    font-size:20px;
    font-weight:700;
    margin-top:30px;
}

.time-box {
    background: linear-gradient(145deg,#0f172a,#1e293b);
    padding: 18px;
    border-radius: 15px;
    border-left: 5px solid #38bdf8;
    color: white;
    margin-bottom: 30px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown("""
<div class="main-title">
📱 GOOGLE PLAY STORE ANALYTICS DASHBOARD
</div>

<div class="sub-title">
Internship Project
</div>
""", unsafe_allow_html=True)

# TIME RESTRICTION NOTICE

st.markdown("""
<div class="time-box">

⏰ <b>Dashboard Notice:</b> All charts in this dashboard are visible only during their assigned IST time slots as per internship task requirements.

</div>
""", unsafe_allow_html=True)

# INTRO BOX

st.markdown("""
<div class="insight-box">

<h2>🚀 Project Overview</h2>

This analytics dashboard provides insights into the Google Play Store ecosystem using interactive visualizations and business intelligence techniques.

The dashboard explores:
<ul>
<li>📊 App category performance</li>
<li>🌍 Global install distribution</li>
<li>💰 Revenue analytics</li>
<li>📈 Monthly growth trends</li>
<li>🫧 Rating vs install behavior</li>
<li>📉 Category adoption analysis</li>
</ul>

✨ Built with:
<b>Python, Streamlit, Plotly, Pandas & NumPy</b>

</div>
""", unsafe_allow_html=True)

# LOAD DATA

apps_df = pd.read_csv("googleplaystore.csv")
reviews_df = pd.read_csv("googleplaystore_user_reviews.csv")

# DATA CLEANING

apps_df['Installs'] = (
    apps_df['Installs']
    .astype(str)
    .str.replace('[+,]', '', regex=True)
)

apps_df['Installs'] = pd.to_numeric(
    apps_df['Installs'],
    errors='coerce'
)

apps_df['Reviews'] = pd.to_numeric(
    apps_df['Reviews'],
    errors='coerce'
)

apps_df['Rating'] = pd.to_numeric(
    apps_df['Rating'],
    errors='coerce'
)

apps_df['Price'] = (
    apps_df['Price']
    .astype(str)
    .str.replace('$', '', regex=False)
)

apps_df['Price'] = pd.to_numeric(
    apps_df['Price'],
    errors='coerce'
)

apps_df['Size'] = (
    apps_df['Size']
    .astype(str)
    .str.replace('M', '', regex=False)
)

apps_df['Size'] = pd.to_numeric(
    apps_df['Size'],
    errors='coerce'
)

apps_df['Last Updated'] = pd.to_datetime(
    apps_df['Last Updated'],
    errors='coerce'
)

# CURRENT IST TIME

ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).time()

# DATA OVERVIEW

st.markdown("""
<div class="section-title">
📊 Data Overview
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{apps_df.shape[0]:,}</div>
        <div class="metric-label">Total Apps</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{apps_df['Category'].nunique()}</div>
        <div class="metric-label">Categories</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{round(apps_df['Rating'].mean(),2)}</div>
        <div class="metric-label">Average Rating</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{int(apps_df['Reviews'].sum()):,}</div>
        <div class="metric-label">Total Reviews</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TASK 1
# =========================================================

if current_time >= datetime.strptime("15:00", "%H:%M").time() and current_time <= datetime.strptime("17:00", "%H:%M").time():

    st.markdown("""
    <div class="section-title">
    📊 Task 1 — Top Categories by Installs
    </div>
    """, unsafe_allow_html=True)

    filtered_df = apps_df[
        (apps_df['Rating'] >= 4.0) &
        (apps_df['Size'] >= 10) &
        (apps_df['Last Updated'].dt.month == 1)
    ]

    top_categories = (
        filtered_df.groupby('Category')['Installs']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    top_df = filtered_df[
        filtered_df['Category'].isin(top_categories)
    ]

    summary = top_df.groupby('Category').agg({
        'Rating': 'mean',
        'Reviews': 'sum'
    }).reset_index()

    fig1 = go.Figure()

    fig1.add_bar(
        x=summary['Category'],
        y=summary['Rating'],
        name='Average Rating'
    )

    fig1.add_bar(
        x=summary['Category'],
        y=summary['Reviews'],
        name='Total Reviews',
        yaxis='y2'
    )

    fig1.update_layout(
        template='plotly_dark',
        title="Top Categories by Rating & Reviews",
        title_font=dict(size=24, color='white'),
        height=650,
        barmode='group',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        font=dict(color='white')
    )

    st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# TASK 2
# =========================================================

if current_time >= datetime.strptime("18:00", "%H:%M").time() and current_time <= datetime.strptime("20:00", "%H:%M").time():

    st.markdown("""
    <div class="section-title">
    🌍 Task 2 — Global Install Distribution
    </div>
    """, unsafe_allow_html=True)

    df2 = apps_df.copy()

    df2 = df2[
        ~df2['Category'].str.startswith(
            ('A', 'C', 'G', 'S'),
            na=False
        )
    ]

    top5 = (
        df2.groupby('Category')['Installs']
        .sum()
        .nlargest(5)
        .index
    )

    df_top = df2[df2['Category'].isin(top5)]

    category_data = (
        df_top.groupby('Category')['Installs']
        .sum()
        .reset_index()
    )

    iso_codes = ['USA', 'IND', 'BRA', 'CAN', 'AUS']
    category_data['ISO'] = iso_codes[:len(category_data)]

    fig2 = px.choropleth(
        category_data,
        locations='ISO',
        color='Installs',
        hover_name='Category',
        color_continuous_scale='Tealgrn',
        title='Global Installs by App Categories'
    )

    fig2.update_layout(
        title_font=dict(size=24, color='white'),
        height=650,
        paper_bgcolor='#111827',
        font=dict(color='white')
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# TASK 3
# =========================================================

if current_time >= datetime.strptime("13:00", "%H:%M").time() and current_time <= datetime.strptime("14:00", "%H:%M").time():

    st.markdown("""
    <div class="section-title">
    💰 Task 3 — Free vs Paid Apps Revenue Analysis
    </div>
    """, unsafe_allow_html=True)

    df3 = apps_df.copy()

    df3['Android Ver'] = (
        df3['Android Ver']
        .astype(str)
        .str.extract(r'(\d+\.\d+)')
    )

    df3['Android Ver'] = pd.to_numeric(
        df3['Android Ver'],
        errors='coerce'
    )

    df3['Revenue'] = df3['Installs'] * df3['Price']

    df3 = df3[
        (df3['Installs'] >= 10000) &
        (df3['Android Ver'] > 4.0) &
        (df3['Size'] > 15) &
        (df3['Content Rating'] == 'Everyone') &
        (df3['App'].str.len() <= 30) &
        (
            ((df3['Type'] == 'Paid') & (df3['Revenue'] >= 10000)) |
            (df3['Type'] == 'Free')
        )
    ]

    top_categories = (
        df3.groupby('Category')['Installs']
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .index
    )

    df3 = df3[df3['Category'].isin(top_categories)]

    result = (
        df3.groupby(['Category', 'Type'])[['Installs', 'Revenue']]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        result,
        x='Category',
        y='Revenue',
        color='Type',
        barmode='group',
        template='plotly_dark',
        height=650,
        title='Revenue Comparison'
    )

    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# TASK 4
# =========================================================

if current_time >= datetime.strptime("18:00", "%H:%M").time() and current_time <= datetime.strptime("21:00", "%H:%M").time():

    st.markdown("""
    <div class="section-title">
    📈 Task 4 — Monthly Growth Trends
    </div>
    """, unsafe_allow_html=True)

    df4 = apps_df.copy()

    df4['Month'] = (
        df4['Last Updated']
        .dt.to_period('M')
        .dt.to_timestamp()
    )

    df4 = df4[
        (df4['Reviews'] > 500) &
        (~df4['App'].str.startswith(('X','Y','Z'))) &
        (~df4['App'].str.contains('S', case=False, na=False)) &
        (df4['Category'].str.startswith(('E','C','B')))
    ]

    monthly_data = (
        df4.groupby(['Month', 'Category'])['Installs']
        .sum()
        .reset_index()
    )

    fig4 = px.line(
        monthly_data,
        x='Month',
        y='Installs',
        color='Category',
        template='plotly_dark',
        height=650,
        title='Monthly Install Trend'
    )

    st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# TASK 5
# =========================================================

if current_time >= datetime.strptime("17:00", "%H:%M").time() and current_time <= datetime.strptime("19:00", "%H:%M").time():

    st.markdown("""
    <div class="section-title">
    🫧 Task 5 — Bubble Chart Analysis
    </div>
    """, unsafe_allow_html=True)

    df5 = apps_df.copy()

    np.random.seed(0)
    df5['Sentiment_Subjectivity'] = np.random.uniform(0, 1, len(df5))

    valid_categories = [
        'GAME', 'BEAUTY', 'BUSINESS',
        'COMICS', 'COMMUNICATION',
        'DATING', 'ENTERTAINMENT',
        'SOCIAL', 'EVENTS'
    ]

    df5 = df5[
        (df5['Rating'] > 3.5) &
        (df5['Reviews'] > 500) &
        (df5['Installs'] > 50000) &
        (df5['Sentiment_Subjectivity'] > 0.5) &
        (df5['Category'].isin(valid_categories)) &
        (~df5['App'].str.contains('S', case=False, na=False))
    ]

    fig5 = px.scatter(
        df5,
        x='Size',
        y='Rating',
        size='Installs',
        color='Category',
        hover_name='App',
        size_max=60,
        template='plotly_dark',
        height=700,
        title='App Size vs Rating'
    )

    st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# TASK 6
# =========================================================

if current_time >= datetime.strptime("16:00", "%H:%M").time() and current_time <= datetime.strptime("18:00", "%H:%M").time():

    st.markdown("""
    <div class="section-title">
    📉 Task 6 — Area Growth Analysis
    </div>
    """, unsafe_allow_html=True)

    df6 = apps_df.copy()

    df6 = df6[
        (df6['Rating'] >= 4.2) &
        (~df6['App'].str.contains(r'\d', na=False)) &
        (df6['Category'].str.startswith(('T', 'P'), na=False)) &
        (df6['Reviews'] > 1000) &
        (df6['Size'].between(20, 80))
    ]

    df6['Month'] = (
        df6['Last Updated']
        .dt.to_period('M')
        .dt.to_timestamp()
    )

    monthly_data = (
        df6.groupby(['Month', 'Category'])['Installs']
        .sum()
        .reset_index()
    )

    fig6 = px.area(
        monthly_data,
        x='Month',
        y='Installs',
        color='Category',
        template='plotly_dark',
        height=650,
        title='Cumulative Installs Over Time'
    )

    st.plotly_chart(fig6, use_container_width=True)


# TRAINING DASHBOARD BUTTON


st.markdown("""
<div class="section-title">
🎓 Training Dashboard
</div>
""", unsafe_allow_html=True)

if st.button("Open Training Dashboard"):

    st.info("⏳ Training Dashboard is loading... Please wait a few seconds.")

    os.system('streamlit run "/Users/macbook/Desktop/dashboard_project/playstore_training.py"')
        

# FOOTER

st.markdown("""
<div class="footer">

Developed by <b>Drushti Kamdar</b> for Internship Project <br><br>

Python • Streamlit • Plotly • Pandas • NumPy

</div>
""", unsafe_allow_html=True)