import streamlit as st
import pandas as pd


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('MVP_NUTRITION_4_2_2024.csv',on_bad_lines='skip',low_memory=False)

df.index = range(1,len(df)+1)
st.set_page_config(
   page_title="NutrAGI - Nutritional Assistant",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.title("NutrAGI - Nutritional Assistant")
st.subheader ("Meal Suggestion and Traking App")

col1,col2,col3,col4=st.columns(4)
col11,col12,col13,col14=st.columns(4)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df.columns = df.columns.str.replace('_', ' ')
df.rename(columns={"R": "Restaurant", "M": "Supermarket", "H": "Home", "P": "Preferred", "I": "Indifferent", "K": "Avoid", "Q":"Quantity","C": "Cost"},inplace=True)
df.columns=df.columns.str.capitalize()


#st.line_chart(sol)
with col1:
    meal = st.radio(
        "Choose meal type",
        ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack","Dinner", "Evening Snack", "Other"]
    )

with col11:
    st.write("You selected:",meal)
with col2:
    location = st.radio(
        "Location of the meal",
        ['Restaurant', 'Supermarket','Home','Other']
)
    R = st.checkbox('Restaurant')
    M = st.checkbox('Super Market')
    H = st.checkbox('Home')
    O = st.checkbox('Other')

with col12:    
    st.write("Your location is:", location)
with col3:
    preference = st.radio(
        'Select the level of likeness of food',
        ['Preferred', 'Indifferent','Avoid','Other']
        
)
with col13:
    st.write('You selected:', preference)

dfsol=df[(df[meal]==1)&(df[location]==1)&(df[preference]==1)]
with st.expander("Food List available for your choise"):
    st.dataframe(dfsol)

today_nutr=list(dfsol.Name)
#today_nutr
with col4:
    y = st.multiselect (
        "Food Selector (Select Food Number from dropDown Menu)",
        today_nutr                   
    )

    sol=dfsol[dfsol["Name"].isin(y)].T
cola,col1b=st.columns(2)

with cola:
    #sol=df1.loc[:, ~(df1 == 0).all()].T
    sol['Total'] = sol.iloc[2::].sum(axis = 1)
    #sol['Total'] = sol['Total'].fillna('')
    sol=sol.loc[['Name', 'Breakfast', 'Snack', 'Restaurant', 'Supermarket', 'Cost',
              'Serving size', 'Quantity', 'Calories', 'Fat','Total fat', 'Saturated fat',
                'Cholesterol', 'Sodium', 'Choline', 'Folate', 'Niacin', 'Pantothenic acid'
                , 'Riboflavin', 'Thiamin', 'Carotene alpha', 'Vitamin b12', 'Vitamin b6', 
                'Vitamin c', 'Vitamin d', 'Vitamin e', 'Vitamin k', 'Calcium', 'Copper', 
                'Iron', 'Magnesium', 'Manganese', 'Phosphorous', 'Potassium', 'Selenium', 
                'Zink', 'Protein', 'Carbohydrate', 'Fiber', 'Glucose', 'Sucrose',
                  'Alcohol', 'Ash', 'Water']]
    with st.expander("Food Consumed"):
            st.dataframe(sol)
total_cost=format(sol.Total.Cost,'.2f')
cola1,colb1,colc1,cold1, cole1,colf1=st.columns(6)
with col1b:
    with cola1:
        st.metric(label="Cost ($)", value=format(sol.Total.Cost,'.2f'))
    with colb1:
        st.metric(label="Protein (gr)", value=format(sol.Total.Protein,'.2f'))
    with colc1:
        st.metric(label="Calories (gr.)", value=format(sol.Total.Calories,'.2f'))
    with cold1:
        st.metric(label="Carbohydrate (gr.)", value=format(sol.Total.Carbohydrate,'.2f'))
    with cole1:
        st.metric(label="Fat (gr.)", value=format(sol.Total.Fat,'.2f'))
    with colf1:
        st.metric(label="Fiber (gr.)", value=format(sol.Total.Fiber,'.2f'))
    with cola1:
        st.metric(label="Cholesterol (mg.)", value=format(sol.Total.Cholesterol,'.2f'))





     
