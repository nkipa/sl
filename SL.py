import streamlit as st
import pandas as pd
from io import StringIO


hist_nut_path = 'hist_nut.csv'
selected_df = pd.DataFrame()

# Set display options once
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)





# Load and prepare the DataFrame
df = pd.read_csv('nutra.csv', on_bad_lines='skip', low_memory=False)
df.index = range(1, len(df) + 1)
df.columns = df.columns.str.replace('_', ' ').str.capitalize()
df.rename(columns={"R": "Restaurant", "M": "Supermarket", "H": "Home", 
                   "P": "Preferred", "I": "Indifferent", "K": "Avoid", 
                   "Q": "Quantity", "C": "Cost"}, inplace=True)

# Streamlit page config
st.set_page_config(page_title="NutrAGI - Nutritional Assistant", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")

st.title("NutrAGI - Nutritional Assistant")
st.subheader("Meal Suggestion and Tracking App")

with st.sidebar:
    title = st.markdown( '''INSTRUCTIONS  
                        
    1. Select one MEAL TYPE. 
       (Breakfast,  Morning Snack, etc)
    2. Next Select the LOCATION.
        (Restaurant, Supermaket.., etc)
    3. Then Select PREFERENCES.
    4. Select FOOD ITEM from the
       dropdown list, once you are done
    5. Press "Record Meal" button
    6. Repeat Steps 1 to 5 for the
       next meal of the day
    7. At the end of the day
       press "End of Day Processing"
       A new button will apear
       "Download Historical Data.."
       '''

    )   

meal_map = {"Morning Snack": "Snack", "Afternoon Snack": "Snack", "Evening Snack": "Snack"}
columns = [st.columns(4) for _ in range(2)]  # Generate two rows of columns

meal = columns[0][0].radio("Choose meal type", ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Evening Snack", "Other"])
real_meal=meal
meal = meal_map.get(meal, meal)  # Simplify snack types
columns[1][0].write(f"You selected: {meal}")

location = columns[0][1].radio("Location of the meal", ['Restaurant', 'Supermarket', 'Home', 'Other'])
columns[1][1].write(f"Your location is: {location}")

preference = columns[0][2].radio('Select the level of likeness of food', ['Preferred', 'Indifferent', 'Avoid', 'Other'])
columns[1][2].write(f'You selected: {preference}')

record_button_col = columns[1][3] 
end_day_button_col = columns[1][3]
dload_button = columns[1][3]


# Filter DataFrame based on selections
dfsol = df[(df[meal] == 1) & (df[location] == 1) & (df[preference] == 1)]

with st.expander("Food List available for your choice"):
    st.dataframe(dfsol)

today_nutr = list(dfsol.Name)

y = columns[0][3].multiselect("Food Selector (Select Food Number from dropDown Menu)", today_nutr)
sol = dfsol[dfsol["Name"].isin(y)].T
sol.columns = sol.iloc[0]
sol = sol[1:]



raw_data = dfsol[dfsol["Name"].isin(y)]


raw_data= raw_data.copy()

raw_data["Meal"] = real_meal
raw_data["Location"] = location
raw_data["Preference"] = preference
first_column = raw_data.pop('Meal')
second_column= raw_data.pop('Location')
third_column = raw_data.pop('Preference')
raw_data.insert(0, 'Meal', first_column)
raw_data.insert(1, 'Location', second_column)
raw_data.insert(2, 'Preference', third_column)


# Adjust and display total nutritional info
sol['Total'] = sol.iloc[2:].sum(axis=1)
relevant_columns = ['Breakfast', 'Lunch', 'Dinner', 'Snack',
                    'Restaurant', 'Supermarket', 'Cost', 'Serving size',
                    'Quantity', 'Calories', 'Fat', 'Total fat',
                    'Saturated fat', 'Cholesterol', 'Sodium', 'Choline',
                    'Folate', 'Niacin', 'Pantothenic acid', 'Riboflavin',
                    'Thiamin', 'Carotene alpha', 'Vitamin b12', 'Vitamin b6',
                    'Vitamin c', 'Vitamin d', 'Vitamin e', 'Vitamin k', 'Calcium',
                    'Copper', 'Iron', 'Magnesium', 'Manganese', 'Phosphorous',
                    'Potassium', 'Selenium', 'Zink', 'Protein', 'Carbohydrate', 
                    'Fiber', 'Glucose']
sol = sol.loc[relevant_columns]
with st.expander("Food Consumed"):
    selected_meal_df=st.dataframe(sol)



# Calculating and displaying total values in a more structured way
metrics_columns = st.columns(8)
metrics = [("Cost ($)", "Cost"), ("Protein (gr)", "Protein"), ("Calories", "Calories"),
           ("Carbohydrate (gr.)", "Carbohydrate"), ("Fat (gr.)", "Fat"), ("Fiber (gr.)", "Fiber"),
           ("Cholesterol (mg.)", "Cholesterol"),("Sodium (mg.)","Sodium")]

def record_meal(food):
# Check if there's already meal data stored in the session state
    if 'intermediary_data' not in st.session_state:
        st.session_state['intermediary_data'] = food
    else:
        # Ensure both objects are DataFrames before concatenation
        st.session_state['intermediary_data'] = pd.concat([st.session_state['intermediary_data'], raw_data], ignore_index=True)

# Function to append data to an in-memory CSV (session state) instead of a physical file
def record_meal_intermediary(meal_info):
    # Check if there's already meal data stored in the session state
    if 'intermediary_data' not in st.session_state:
        st.session_state['intermediary_data'] = meal_info
    else:
        # Ensure both objects are DataFrames before concatenation
        st.session_state['intermediary_data'] = pd.concat([st.session_state['intermediary_data'], raw_data], ignore_index=True)

# Function to append session state data to historical data, this is conceptual, as actual file writes are avoided
def end_of_day_processing(historical_filename='historical_meals.csv'):
    if 'intermediary_data' in st.session_state and not st.session_state['intermediary_data'].empty:
        # Conceptual placeholder for appending to historical data
        # In practice, this would append the session state data to a DataFrame representing historical data
        # For demonstration, we'll just download the combined data
        historical_df = pd.DataFrame()  # Replace with actual read from historical data source
        combined_df = pd.concat([historical_df, st.session_state['intermediary_data']], ignore_index=True)
        csv = combined_df.to_csv(index=False)
        dload_button.download_button(label="Download Historical Data as CSV", data=csv, file_name=historical_filename, mime='text/csv')
        del st.session_state['intermediary_data']
        st.success('All meals have been saved to the historical record.')

for col, (label, key) in zip(metrics_columns, metrics):
    value = format(sol['Total'].get(key, 0), '.2f')
    col.metric(label=label, value=value)


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(raw_data) 

if record_button_col.button('Record Meal'):
    # Ensure that the operation within this block does not try to treat the button itself as data.
    record_meal_intermediary(raw_data)
    st.success('Meal recorded.')

    
if end_day_button_col.button('End of Day Processing'):
 
    end_of_day_processing()






     





     
