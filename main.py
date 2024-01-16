

# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
import mysql.connector as mysql
from dash import html
import matplotlib.pyplot as plt


# Setting up page configuration
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   )
# Set page background color

background_color = "!Important"  # Replace this with your desired color code
page_bg = f"""
    <style>
        .main {{
            background-color: {background_color};
        }}
    </style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
st.image("img.png")
st.sidebar.markdown("<h1 style='color: #391c59;  font-size: 30px;'>PhonePe Pulse</h1>", unsafe_allow_html=True)






mydb = mysql.connect(host="localhost", user="root", password="", database="phonepe", port =3306
                  )
mydb = mysql.connect(host="localhost", user="root", password="", database="phonepe", port =3306
                  )





mycursor = mydb.cursor(buffered=True)





# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("PhonePe Pulse", ["Home","Top Charts","Explore Data"], 
                icons=["house","graph-up-arrow","bar-chart-line"],
                menu_icon= "cast",
                default_index=0,
                styles={"nav-link": {"font-family":"Roboto", "font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F99AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    #st.image("img.png")
    
    col1,col2 = st.columns([4,1],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
       
#MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        if Type =="Transactions":
         st.info("Top 10 Transactions")
         mycursor.execute(f"SELECT state,sum(transaction_count) as Total FROM `agg_transaction` where year_data={Year} and quarter ={Quarter} group by state order by sum(transaction_count) DESC LIMIT 10;")
         df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'count'])
         st.table(df)
        if Type=="Users":
         st.info(f"Registered users by Quarter") 
         mycursor.execute("SELECT quarter, sum(registeredUser) from map_user group by quarter")  
         df = pd.DataFrame(mycursor.fetchall(), columns=['quarter', 'count'])
         st.table(df)

        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(transaction_count) as Total_count, sum(transaction_amount) as Total from agg_transaction where year_data = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'transaction_count','transaction_amount'])
            fig = px.pie(df, values='transaction_amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['transaction_count'],
                             labels={'transaction_count':'transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district , sum(count_map) as Total_Count, sum(amount) as Total from map_transaction where year_data = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['district', 'transaction_count','transaction_amount'])

            fig = px.pie(df, values='transaction_amount',
                             names='district',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['transaction_count'],
                             labels={'transaction_count':'transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select pincode, sum(transaction_count) as Total_transaction_count, sum(transaction_amount) as Total from top_transaction where year_data = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'transaction_count','transaction_amount'])
            fig = px.pie(df, values='transaction_amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['transaction_count'],
                             labels={'transaction_count':'transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count_agg) as Total_Count, avg(percentage_agg)*100 as Avg_Percentage from agg_user where year_data = {Year} and quarter = {Quarter} group by brands order by Total_Count limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(registeredUser) as Total_Users, sum(appOpens) as Total_Appopens from map_user where year_data = {Year} and quarter = {Quarter} group by district order by Total_Users limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(registeredUsers) as Total_Users from top_user where year_data = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(registeredUser) as Total_Users, sum(appOpens) as Total_Appopens from map_user where year_data = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count_map) as Total_Transactions, sum(amount) as Total_amount from map_transaction  where year_data = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('states.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count_map) as Total_Transactions, sum(amount) as Total_amount from map_transaction  where year_data = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['state', 'Total_Transactions', 'Total_amount'])
            print(df1)
            df2 = pd.read_csv('states.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            # df1.State = df2
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['state', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('states.csv')
            print(df1)
            # Plot graph using st.plotly_chart
            
            fig = px.bar(df1, x='state', y='Total_Transactions', color='Total_Transactions', text='Total_Transactions',
            labels={'Total_Transactions': 'Total Transactions'},
            title='Total Transactions by state',
            color_continuous_scale='sunset')

            st.plotly_chart(fig, use_container_width=True)

            

          
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from agg_transaction where year_data= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year_data,quarter, sum(count_map) as Total_Transactions, sum(amount) as Total_amount from map_transaction where year_data = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year_data,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(registeredUser) as Total_Users, sum(appOpens) as Total_Appopens from map_user where year_data = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('states.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year_data,quarter,District,sum(registeredUser) as Total_Users, sum(appOpens) as Total_Appopens from map_user where year_data = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year_data,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year_data', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        

        


