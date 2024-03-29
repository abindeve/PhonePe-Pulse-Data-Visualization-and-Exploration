
import json
import os
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import pydeck as pdk

import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium

from PIL import Image
from git.repo.base import Repo


# Displaying an image as an icon


# Set page title and icon
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | By Abin C Babu",
    page_icon=":bar_chart:",  # Replace with your desired emoji or icon
    layout = "wide"
)
custom_css = """
    body {
        background-color: #000000; /* Change this color to your desired background color */
    }
"""
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
# Custom top navigation bar#220c3f
nav_bar = """
    <div style="display: flex; justify-content: space-between; padding: 1rem; background-color: #391c59; width:100%">
        <div style="font-size: 1.5rem; color:white; font-weight: bold;">Phonepe Pulse</div>
        <div style="display: flex; color:white; gap: 1rem;">
            <div style="cursor: pointer;">Home</div>
            <div style="cursor: pointer;">Top Charts</div>
            <div style="cursor: pointer;">Explore Data</div>
            <div style="cursor: pointer;">About</div>
        </div>
    </div>
"""

# Render the custom top navigation bar
st.markdown(nav_bar, unsafe_allow_html=True)




def insert_into_agg_trans(row):

    query = f"""
        INSERT INTO agg_transaction (
            state,
            year_data,
            quarter,
            transaction_type,
            transaction_count,
            transaction_amount
        ) VALUES (
            '{row['State']}',
            {row['Year']},
            {row['Quarter']},
            '{row['Transaction_type']}',
            {row['Transaction_count']},
            '{row['Transaction_amount']}'
        );"""

    return test(query)

def insert_into_agg_user(row):


    query = f"""
            INSERT INTO agg_user (
                state,
                year_data,
                quarter,
                brands,
                count_agg,
                percentage_agg
            ) VALUES (
                '{row['State']}',
                {row['Year']},
                {row['Quarter']},
                '{row['Brands']}',
                {row['Count']},
                '{row['Percentage']}'
            );"""

    return test(query)



def insert_into_map_trans(row, cursor):
    query = f"""
        INSERT INTO map_transaction (
            state,
            year_data,
            quarter,
            amount,
            district,
            count_map
        ) VALUES (
            '{row['State']}',
            {row['Year']},
            {row['Quarter']},
            '{row['Amount']}',
            '{row['District']}',
            {row['Count']}
        );"""

    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error inserting row into map_transaction: {e}")


def insert_into_map_user(row):
    query = f"""
               INSERT INTO map_user (
                   state,
                   year_data,
                   quarter,
                   district,
                   registeredUser,
                   appOpens
               ) VALUES (
                   '{row['State']}',
                   {row['Year']},
                   {row['Quarter']},
                   '{row['District']}',
                   {row['RegisteredUser']},
                   {row['AppOpens']}
               );"""

    return test(query)

def insert_into_top_trans(row):

    query = f"""
               INSERT INTO top_transaction (
                   state,
                   year_data,
                   quarter,
                   pincode,
                   transaction_count,
                   transaction_amount
               ) VALUES (
                   '{row['State']}',
                   {row['Year']},
                   {row['Quarter']},
                   {row['Pincode']},
                   {row['Transaction_count']},
                   '{row['Transaction_amount']}'
               );"""
    # ['State', 'Year', 'Quarter', 'Pincode', 'Transaction_count', 'Transaction_amount']
    return test(query)
def insert_into_top_user(row):

    query = f"""
               INSERT INTO top_user (
                   state,
                   year_data,
                   quarter,
                   pincode,
                   registeredUsers              
               ) VALUES (
                   '{row['State']}',
                   {row['Year']},
                   {row['Quarter']},
                   {row['Pincode']},
                   '{row['RegisteredUsers']}'                  
               );"""
    # ['State', 'Year', 'Quarter', 'Pincode', 'RegisteredUsers']
    return test(query)
def connect_mysql():
    connection = mysql.connector.connect(
        host="localhost", user="root", password="", database="phonepe",port = 3306
    )
    return connection

def test(query):

    mysql_connection = connect_mysql()
    cursor = mysql_connection.cursor()
    cursor.execute(query)
    mysql_connection.commit()  # Commit changes
    cursor.close()
    mysql_connection.close()

def create_aggregated_tansaction(path, column_names):
    data_list = []
    transaction_list = os.listdir(path)

    for state in transaction_list:
        p_state = os.path.join(path, state)
        year_list = os.listdir(p_state)
        for year in year_list:
            p_year = os.path.join(p_state, year)
            quarter_list = os.listdir(p_year)
            for quarter in quarter_list:
                p_quarter = os.path.join(p_year, quarter)
                data_file = open(p_quarter, 'r')
                data = json.load(data_file)

                try:
                    for transaction_data in data['data']['transactionData']:
                        name = transaction_data['name']
                        count = transaction_data['paymentInstruments'][0]['count']
                        amount = transaction_data['paymentInstruments'][0]['amount']
                        row_data = [state, year, int(quarter.strip('.json')), name, count, amount]
                        data_list.append(row_data)
                except:
                    pass

    return pd.DataFrame( data_list, columns=column_names)



def create_aggregated_user(path_user, column_names_user):
    data_list=[]
    user_list = os.listdir(path_user)

    for state in user_list:
        p_state = os.path.join(path_user, state)
        year_list = os.listdir(p_state)
        for year in year_list:
            p_year = os.path.join(p_state, year)
            quarter_list = os.listdir(p_year)
            for quarter in quarter_list:
                p_quarter = os.path.join(p_year, quarter)
                data_file = open(p_quarter, 'r')
                datas = json.load(data_file)


                try:
                    for value in datas["data"]["usersByDevice"]:
                        brand_name = value["brand"]
                        percentage = value["percentage"]
                        count = value["count"]
                        row_data = [state,year,int(quarter.strip('.json')),brand_name,count,percentage ]
                        data_list.append(row_data)
                except:
                    pass
    return pd.DataFrame( data_list, columns=column_names_user)

def create_map_transaction(path_map_transaction,column_names_transaction):
    data_list=[]
    map_trx_list = os.listdir(path_map_transaction)
    for state in map_trx_list:
        p_state = os.path.join(path_map_transaction, state)
        year_list = os.listdir(p_state)
        for year in year_list:
            p_year = os.path.join(p_state, year)
            quarter_list = os.listdir(p_year)
            for quarter in quarter_list:
                p_quarter = os.path.join(p_year, quarter)
                data_file = open(p_quarter, 'r')
                data = json.load(data_file)
                try:
                    for value in data["data"]["hoverDataList"]:
                        district = value['name']
                        count = value['metric'][0]['count']
                        amount = value['metric'][0]['amount']
                        row_data = [state,year,int(quarter.strip('.json')),amount,district,count]
                        data_list.append(row_data)
                except:
                    pass
    return pd.DataFrame(data_list,columns=column_names_transaction)


def create_map_user(path_map_user, column_map_user):
    data_list=[]
    map_user_list = os.listdir(path_map_user)
    for state in map_user_list:
        p_state = os.path.join(path_map_user, state)
        year_list = os.listdir(p_state)
        for year in year_list:
            p_year = os.path.join(p_state, year)
            quarter_list = os.listdir(p_year)
            for quarter in quarter_list:
                p_quarter = os.path.join(p_year, quarter)
                data_file = open(p_quarter, 'r')
                data = json.load(data_file)
                # print(data)
                try:
                    for value in data["data"]["hoverData"].items():
                        district = value[0]
                        registereduser = value[1]["registeredUsers"]
                        appOpens = value[1]["appOpens"]
                        row_data = [state,year,int(quarter.strip('.json')),district,registereduser,appOpens]
                        data_list.append(row_data)
                except:
                    pass
    return pd.DataFrame(data_list,columns=column_map_user)



def create_top_transaction(path5):
    top_trans_list = os.listdir(path5)
    columns5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
                'Transaction_amount': []}

    for state in top_trans_list:
        cur_state = path5 + state + "/"
        top_year_list = os.listdir(cur_state)

        for year in top_year_list:
            cur_year = cur_state + year + "/"
            top_file_list = os.listdir(cur_year)

            for file in top_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                E = json.load(data)

                for i in E['data']['pincodes']:
                    name = i['entityName']
                    count = i['metric']['count']
                    amount = i['metric']['amount']
                    columns5['Pincode'].append(name)
                    columns5['Transaction_count'].append(count)
                    columns5['Transaction_amount'].append(amount)
                    columns5['State'].append(state)
                    columns5['Year'].append(year)
                    columns5['Quarter'].append(int(file.strip('.json')))
        df_top_trans = pd.DataFrame(columns5)
    return df_top_trans
def create_top_user(path_top_user, column_top_user):
    data_list =[]
    top_user = os.listdir(path_top_user)
    for state in top_user:
        p_state = os.path.join(path_top_user,state)
        year_list = os.listdir(p_state)

        for year in year_list:
            p_year = os.path.join(p_state,year)
            quarter_list = os.listdir(p_year)

            for quarters in quarter_list:
                p_quarter = os.path.join(p_year, quarters)
                data_file = open(p_quarter, 'r')
                data = json.load(data_file)

                for value in data['data']['pincodes']:
                    name = value['name']
                    registeredUsers = value['registeredUsers']
                    row_data = [state,year,int(quarters.strip('.json')),name,registeredUsers]
                    data_list.append(row_data)



    return pd.DataFrame(data_list,columns=column_top_user)


path_top_user = "pulse/data/top/user/country/india/state/"
column_top_user = ['State','Year','Quarter','z','RegisteredUsers']
top_user = create_top_user(path_top_user, column_top_user)
st.write("Top User")
st.write(top_user)

# Create a colorful bar chart
fig, ax = plt.subplots(figsize=(12, 6))

# Group by State and sum RegisteredUsers
state_totals = top_user.groupby('State')['RegisteredUsers'].sum()

# Define a colormap for the bars
colors = plt.cm.viridis(state_totals / max(state_totals))

# Plotting a bar chart with colorful bars
state_totals.plot(kind='bar', ax=ax, color=colors)

ax.set_xlabel("State")
ax.set_ylabel("Registered Users")
ax.set_title("Registered Users by State with Colorful Bars")

# Display the colorful bar chart in Streamlit
st.pyplot(fig)

