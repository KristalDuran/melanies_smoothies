# Import python packages
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

st.title(f":cup_with_straw: My parents new healthy Dinner! :cup_with_straw:")

name = st.text_input("Name on Smoothie", "")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if len(ingredients_list) <= 5:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
