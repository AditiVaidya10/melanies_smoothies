import streamlit as st
import os
from snowflake.snowpark.functions import col

st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)

ingredients_string = ''
for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

time_to_insert = st.button('Submit Order')

if time_to_insert:
    if ingredients_string and name_on_order:
        session.sql(
            "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (:1, :2)",
            params=[ingredients_string.strip(), name_on_order]
        ).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
