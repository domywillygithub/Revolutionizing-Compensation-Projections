import streamlit as st
import pickle 
import numpy as np 
import warnings 
warnings.filterwarnings('ignore')


def load_model():
    with open('saves_steps.pkl', 'rb') as file:
        data=pickle.load(file)

    return data

data = load_model()

regressor_loaded = data['model']  
le_country = data['le_country']
le_education = data['le_education']

def show_predict_page():
    st.title('Software Developer Salary Prediction')

    st.write("""### Please Enter the Information Below to Predict the Salary""")
    
    countries = (
        'United States of America',                                                                                
        'Germany',                                                  
        'United Kingdom of Great Britain and Northern Ireland',     
        'Canada',                                                  
        'India',                                                   
        'France',                                                 
        'Netherlands',                                              
        'Australia',                                                 
        'Brazil',                                                   
        'Spain',                                                    
        'Sweden',                                                    
        'Italy',                                                   
        'Poland',                                                    
        'Switzerland',                                               
        'Denmark',                                                  
        'Norway',                                                  
        'Israel'
              )
    
    education =(
        "Bachelor's degree", 
        'Less than a Bachelor', 
        "Master's degree",
       'Post grad'
    )

    countries = st.selectbox('Country',countries)

    education = st.selectbox('Education',education)

    experience = st.slider('Years of Experience', 0,50,3)

    ok = st.button('Calculate Salary')

    if ok:
        x = np.array([[countries, education, experience]])
        x[:, 0] = le_country.transform(x[:, 0])
        x[:, 1] = le_education.transform(x[:,1])
        x = x.astype(float)

        salary = regressor_loaded.predict(x)

        st.subheader(f'Estimated Salary is  ${salary[0]:.2f}')
