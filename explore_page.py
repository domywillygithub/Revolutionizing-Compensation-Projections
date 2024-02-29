import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for x in range(len(categories)):
        if categories.values[x] >= cutoff:
            categorical_map[categories.index[x]] = categories.index[x]
            
        else:
            categorical_map[categories.index[x]] = 'Other'
            
    return categorical_map 

def clean_experience(x):
    if x == 'Less than 1 year':
        return 0.5
    if x == 'More than 50 years':
        return 50
    return float(x)

def clean_education(x):
    if 'Bachelor`s degree (B.A., B.S., B.Eng., etc.)' in x:
        return "Bachelor's degree"
    
    if 'Master`s degree (M.A., M.S., M.Eng., MBA, etc.)' in x:
        return "Master's degree"
    
    if "Professional degree" in x:
        return 'Post grad'
    
    return 'Less than a Bachelor'

@st.cache_data #it executes it only once 
def load_data():
    df=pd.read_csv('survey_results_public.csv')
    columns = ['Country', 'EdLevel','YearsCodePro','Employment','ConvertedCompYearly']

    df=df[columns]
    df=df.rename({'ConvertedCompYearly':'Salary'}, axis=1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment']== 'Employed, full-time']

    df = df.drop('Employment', axis=1)
    country_map = shorten_categories(df.Country.value_counts(), 400)

    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]

    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education) 

    return df 

df = load_data()

def show_explore_page():
    st.title('Explore Software Developer Salaries')

    st.write("""
             ### Stack Overflow Developer Survey 2023
             """)
    
    data = df['Country'].value_counts()


    st.write(""" ### Number of Data from different countries""")

    data = data.to_frame(name = 'Data numbers').reset_index()
    data = data.rename(columns={'index': 'Country'})
    st.table(data)
    

    st.write(""" ### Average Salary Based on Country""")

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True).reset_index()
    data['Salary'] = (data['Salary'] / 1000).round(2)
   
    data['text'] = data['Salary'].astype(str) + 'k'

    fig = px.bar(data, x='Salary', y='Country', text='text', template='seaborn', orientation="h", color_discrete_sequence=['indigo'],  
                height=600, width=900) 
    fig.update_traces(textposition='inside', textfont=dict(color='white', size=18))  
    fig.update_layout(
        xaxis_title="Mean Salary (in k)",
        yaxis_title="Country",
        yaxis=dict(showgrid=False), 
        xaxis=dict(showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True, height=200)

    st.write(""" ### Average Salary Based on Years of Coding Experience""")
    data = df.groupby(['YearsCodePro'])['Salary'].mean().reset_index()
    data = data.rename(columns={'index': 'YearsCodePro'})
    data.sort_values(by = 'YearsCodePro', ascending=True)
    fig = px.line(data, x= 'YearsCodePro', y= 'Salary', template='seaborn', color_discrete_sequence=['green'])  
    fig.update_xaxes(title="Years of Professional Coding Experience", showgrid=False, dtick=2)  
    fig.update_yaxes(title = 'Average Salary', showgrid=False) 
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)