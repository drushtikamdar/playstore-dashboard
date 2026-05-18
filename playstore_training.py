# Generated from: playstore training.ipynb
# Converted at: 2026-05-18T13:33:50.682Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import webbrowser
import os

nltk.download('vader_lexicon')

apps_df = pd.read_csv('googleplaystore.csv')
reviews_df = pd.read_csv('googleplaystore_user_reviews.csv')  # keep this if you also have the reviews file

apps_df.head()

reviews_df.head()

#Step 2 : Data Cleaning
apps_df = apps_df.dropna(subset=['Rating'])
for column in apps_df.columns :
    apps_df[column].fillna(apps_df[column].mode()[0], inplace=True)

apps_df.drop_duplicates(inplace=True)

apps_df = apps_df = apps_df[apps_df['Rating'] <= 5]

reviews_df.dropna(subset=['Translated_Review'], inplace=True)

apps_df.dtypes

#Convert the Installs columns to numeric by removing commas and +
apps_df['Installs'] = apps_df['Installs'].str.replace(',', '').str.replace('+', '').astype(int)

#Convert Price column to numeric after removing $
apps_df['Price'] = apps_df['Price'].str.replace('$', '').astype(float)

apps_df.dtypes

merged_df = pd.merge(apps_df, reviews_df, on='App', how='inner')

merged_df.head()

def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024
    else:
        return np.nan

apps_df['Size'] = apps_df['Size'].apply(convert_size)

apps_df

#Lograrithmic
apps_df['Log_Installs'] = np.log(apps_df['Installs'])

apps_df['Reviews'] = apps_df['Reviews'].astype(int)

apps_df['Log_Reviews'] = np.log(apps_df['Reviews'])

apps_df.dtypes

def rating_group(rating):
    if rating >= 4:
        return 'Top rated app'
    elif rating >= 3:
        return 'Above average'
    elif rating >= 2:
        return 'Average'
    else:
        return 'Below Average'

apps_df['Rating_Group'] = apps_df['Rating'].apply(rating_group)

apps_df['Revenue'] = apps_df['Price'] * apps_df['Installs']

#Revenue column
apps_df['Revenue'] = apps_df['Price'] * apps_df['Installs']

sia = SentimentIntensityAnalyzer()

#Polarity Scores in SIA
#Positive, Negative, Neutral and Compound: -1 = Very negative ; +1 = Very positive

review = "This app is amazing! I love the new features."
sentiment_score = sia.polarity_scores(review)
print(sentiment_score)

review = "This app is very bad! I hate the new features."
sentiment_score = sia.polarity_scores(review)
print(sentiment_score)

review = "This app is okay."
sentiment_score = sia.polarity_scores(review)
print(sentiment_score)


reviews_df['Sentiment_Score'] = reviews_df['Translated_Review'].apply(
    lambda x: sia.polarity_scores(str(x))['compound']
)

reviews_df.head()

apps_df['Last Updated'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')

apps_df['Year'] = apps_df['Last Updated'].dt.year

apps_df.head()

import nltk

nltk.download('vader_lexicon')

html_files_path = "./"
if not os.path.exists(html_files_path):
    os.makedirs(html_files_path)

plot_containers = ""

def save_plot_as_html(fig, filename, insight):
    global plot_containers
    filepath = os.path.join(html_files_path, filename)
    html_content = pio.to_html(fig, full_html=False, include_plotlyjs='inline')
    
    plot_containers += f"""
    <div class="plot-container" id="{filename}" onclick="openPlot('{filename}')">
        <div class="plot">{html_content}</div>
        <div class="insights">{insight}</div>
    </div>
    """
    
    fig.write_html(filepath, full_html=False, include_plotlyjs='inline')

plot_width = 400
plot_height = 300
plot_bg_color = "black"
text_color = "white"
title_font = {'size': 16}
axis_font = {'size': 12}


# Figure 1
category_counts = apps_df['Category'].value_counts().nlargest(10)

fig1 = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    labels={'x': 'Category', 'y': 'Count'},
    title='Top Categories on Play Store',
    color=category_counts.index,
    color_discrete_sequence=px.colors.sequential.Plasma,
    width=400,
    height=300
)

fig1.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

#fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white', width=1))))

save_plot_as_html(
    fig1,
    "Category Graph 1.html",
    "The top categories on the Play Store are dominated by tools, entertainment, and productivity apps"
)

#Figure 2
type_counts = apps_df['Type'].value_counts()

fig2 = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title='App Type Distribution',
    color_discrete_sequence=px.colors.sequential.RdBu,
    width=400,
    height=300
)

fig2.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig2,
    "Type Graph 2.html",
    "Most apps on the Playstore are free, indicating a strategy to attract users first and monetize through ads or in-app purchases."
)

#Figure 3
fig3 = px.histogram(
    apps_df,
    x='Rating',
    nbins=20,
    title='Rating Distribution',
    color_discrete_sequence=['#636EFA'],
    width=400,
    height=300
)

fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig3,
    "Rating Graph 3.html",
    "Ratings are skewed towards higher values, suggesting that most apps are rated favorably by users"
)

#Figure 4
sentiment_counts = reviews_df['Sentiment_Score'].value_counts()

fig4 = px.bar(
    x=sentiment_counts.index,
    y=sentiment_counts.values,
    labels={'x': 'Sentiment Score', 'y': 'Count'},
    title='Sentiment Distribution',
    color=sentiment_counts.index,
    color_discrete_sequence=px.colors.sequential.RdPu,
    width=400,
    height=300
)

fig4.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig4,
    "Sentiment Graph 4.html",
    "Sentiments in reviews show a mix of positive and negative feedback, with a slight lean towards positive sentiment."
)

#Figure 5
installs_by_category = apps_df.groupby('Category')['Installs'].sum().nlargest(10)

fig5 = px.bar(
    x=installs_by_category.index,
    y=installs_by_category.values,
    orientation='h',
    labels={'x': 'Installs', 'y': 'Category'},
    title='Installs by Category',
    color=installs_by_category.index,
    color_discrete_sequence=px.colors.sequential.Blues,
    width=400,
    height=300
)

fig5.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig5,
    "Installs Graph 5.html",
    "The categories with the most installs are social and communication apps, reflecting their broad appeal and high user demand."
)

# Updates Per Year Plot
updates_per_year = apps_df['Last Updated'].dt.year.value_counts().sort_index()

fig6 = px.line(
    x=updates_per_year.index,
    y=updates_per_year.values,
    labels={'x': 'Year', 'y': 'Number of Updates'},
    title='Number of Updates Over the Years',
    color_discrete_sequence=['#AB63FA'],
    width=plot_width,
    height=plot_height
)

fig6.update_layout(
    plot_bgcolor=plot_bg_color,
    paper_bgcolor=plot_bg_color,
    font_color=text_color,
    title_font=title_font,
    xaxis=dict(title_font=axis_font),
    yaxis=dict(title_font=axis_font),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig6,
    "updates_per_year.html",
    "Updates have been increasing over the years, showing that developers are actively maintaining and improving their applications."
)

#Figure 7
revenue_by_category = apps_df.groupby('Category')['Revenue'].sum().nlargest(10)

fig7 = px.bar(
    x=installs_by_category.index,
    y=installs_by_category.values,
    labels={'x': 'Category', 'y': 'Revenue'},
    title='Revenue by Category',
    color=installs_by_category.index,
    color_discrete_sequence=px.colors.sequential.Greens,
    width=400,
    height=300
)

fig7.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig7,
    "Revenue Graph 7.html",
    "Categories such as Business and Productivity lead in revenue generation, indicating their monetization potential."
)

#Figure 8
genre_counts = apps_df['Genres'].str.split(';', expand=True).stack().value_counts().nlargest(10)

fig8 = px.bar(
    x=genre_counts.index,
    y=genre_counts.values,
    labels={'x': 'Genre', 'y': 'Count'},
    title='Top Genres',
    color=installs_by_category.index,
    color_discrete_sequence=px.colors.sequential.OrRd,
    width=400,
    height=300
)

fig8.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig8,
    "Genre Graph 8.html",
    "Action and Casual genres are the most common, reflecting user preferences and market trends."
)

#Figure 9
fig9 = px.scatter(
    apps_df,
    x='Last Updated',
    y='Rating',
    color='Type',
    title='Impact of Last Update on Rating',
    color_discrete_sequence=px.colors.qualitative.Vivid,
    width=400,
    height=300
)

fig9.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig9,
    "Update Graph 8.html",
    "The Scatter Plot shows a weak correlation between the last update and ratings."
)

#Figure 10
fig10 = px.box(
    apps_df,
    x='Type',
    y='Rating',
    color='Type',
    title='Rating for Paid vs Free Apps',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    width=400,
    height=300
)

fig10.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)

save_plot_as_html(
    fig10,
    "Paid Free Graph 10.html",
    "Paid apps generally have higher ratings compared to free apps, suggesting that users expect higher quality from paid applications."
)

plot_containers_split=plot_containers.split('</div>')

if len(plot_containers_split) > 1:
    final_plot = plot_containers_split[-2] + '</div>'
else:
    final_plot = plot_containers

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title> Google Play Store Review Analytics</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #333;
            color: #fff;
            margin: 0;
            padding: 0;
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-color: #444
        }}
        .header img {{
            margin: 0 10px;
            height: 50px;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            justify_content: center;
            padding: 20px;
        }}
        .plot-container {{
            border: 2px solid #555
            margin: 10px;
            padding: 10px;
            width: {plot_width}px;
            height: {plot_height}px;
            overflow: hidden;
            position: relative;
            cursor: pointer;
        }}
        .insights {{
            display: none;
            position: absolute;
            right: 10px;
            top: 10px;
            background-color: rgba(0,0,0,0.7);
            padding: 5px;
            border-radius: 5px;
            color: #fff;
        }}
        .plot-container:hover .insights {{
            display: block;
        }}
    </style>
    <script>
        function openPlot(filename) {{
            window.open(filename, '_blank');
        }}
    </script>
</head>
<body>
    <div class="header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Logo_2013_Google.png/800px-Logo_2013_Google.png" alt="Google Logo">
        <h1>Google Play Store Reviews Analytics</h1>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Google_Play_Store_badge_EN.svg/1024px-Google_Play_Store_badge_EN.svg.png">
    </div>
    <div class="container">
        {plots}
    </div>
</body>
</html>
"""

final_html = dashboard_html.format(
    plots=plot_containers,
    plot_width=plot_width,
    plot_height=plot_height
)

dashboard_path = os.path.join(html_files_path, "web page.html")

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(final_html)

webbrowser.open('file:///' + os.path.realpath(dashboard_path))