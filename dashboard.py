import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

st.set_page_config(page_title='Bike Rental Dashboard', page_icon=':bar_chart:')

hour_df = pd.read_csv("for_dashboard.csv")


st.sidebar.image("Bike Image.jpg")

st.markdown('---')

st.sidebar.header('Please filter here:')
year_cnt = st.sidebar.multiselect(
    'Select year:',
    options=hour_df['yr'].unique(),
    default=hour_df['yr'].unique()
)

month_cnt = st.sidebar.multiselect(
    'Select month:',
    options=hour_df['month_name'].unique(),
    default=hour_df['month_name'].unique()
)

season_cnt = st.sidebar.multiselect(
    'Select season:',
    options=hour_df['season'].unique(),
    default=hour_df['season'].unique()
)

hour_group = st.sidebar.multiselect(
    'Select hour:',
    options=hour_df['bin1'].unique(),
    default=hour_df['bin1'].unique()
)


df_selection = hour_df.query(
    'yr == @year_cnt & month_name == @month_cnt & season == @season_cnt & bin1 == @hour_group'
)




#total_cnt = df_selection['cnt'].sum()


st.title(':bar_chart: Bike Rental Dashboard')

st.markdown('##')

# KPI untuk total penyewaan sepeda

total_cnt = df_selection['cnt'].sum()

st.subheader('Total Rent')
st.subheader(f'{total_cnt:,}')

st.markdown('---')

daily_count_df = df_selection.groupby(by='dteday')['cnt'].sum().reset_index()

daily_count_df['dteday'] = pd.to_datetime(daily_count_df['dteday'])

fig1 = plt.figure(figsize=(24,12))
plt.plot(daily_count_df['dteday'],daily_count_df['cnt'] )
plt.xlabel(None)
plt.ylabel(None)

plt.xticks(rotation=90,fontsize=15)
date_format = mdates.DateFormatter('%b-%Y')
plt.gca().xaxis.set_major_formatter(date_format)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

st.pyplot(fig1)

view1,dwn1 = st.columns(2)
with view1:
    expander = st.expander('View daily count data')
    data = df_selection[['dteday','cnt']].groupby(by='dteday')['cnt'].sum()
    expander.write(data)

with dwn1:
    st.download_button('Get Data', data=data.to_csv().encode('utf-8'),file_name='MonthYear.csv',mime='text/csv')

st.markdown('---')
 
col1,col2 = st.columns(2)

with col1:
    st.subheader('Daily avg by workingday')
    
    daily_workingday_df = df_selection.groupby(['dteday','workingday'])['cnt'].sum().reset_index()
    avg_workingday_df = daily_workingday_df.groupby('workingday')['cnt'].mean().round().reset_index()

    fig2 = plt.figure()
    plt.bar(x = avg_workingday_df['workingday'], height = avg_workingday_df['cnt'])

    st.pyplot(fig2)

with col2:
    st.subheader('Daily avg by season')

    daily_season_df = df_selection.groupby(['dteday','season'])['cnt'].sum().reset_index()
    avg_season_df = daily_season_df.groupby('season')['cnt'].mean().round().reset_index()

    fig3 = plt.figure()
    plt.bar(x = avg_season_df['season'], height=avg_season_df['cnt'])

    st.pyplot(fig3)



view2,dwn2,view3,dwn3 = st.columns([0.25,0.1,0.25,0.1])
with view2:
    expander = st.expander('View Data')
    expander.write(avg_workingday_df)

with dwn2:
    st.download_button('Get Data', data=avg_workingday_df.to_csv().encode('utf-8'), file_name='avg_workingday.csv', mime='text/csv')

with view3:
    expander = st.expander('View Data')
    expander.write(avg_season_df)

with dwn3:
    st.download_button('Get Data', data=avg_season_df.to_csv().encode('utf-8'), file_name='avg_season.csv', mime='text/csv')

st.markdown('---')


col3,col4 = st.columns(2)

with col3:
    st.subheader('Total rent by weathersit')

    by_weathersit_df = df_selection.groupby('weathersit')['cnt'].sum().reset_index()
    
    fig4 = plt.figure()
    plt.bar(x = by_weathersit_df['weathersit'], height = by_weathersit_df['cnt'])
    plt.xticks(rotation=90)

    st.pyplot(fig4)

with col4:
    st.subheader('Total by hour')
    by_hour_df = df_selection.groupby('bin1').sum('cnt').sort_values(by='cnt',ascending=True).reset_index()

    fig5 = plt.figure()
    plt.barh(y=by_hour_df['bin1'], width=by_hour_df['cnt'])

    st.pyplot(fig5)

view4,dwn4,view5,dwn5 = st.columns([0.25,0.1,0.25,0.1])
with view4:
    expander = st.expander('View Data')
    expander.write(by_weathersit_df)

with dwn4:
    st.download_button('Get Data', data=by_weathersit_df.to_csv().encode('utf-8'), file_name='by_weathersit.csv', mime='text/csv')

with view5:
    hour_cnt_df = by_hour_df[['bin1','cnt']].sort_values(by='cnt', ascending=False)

    expander = st.expander('View Data')
    expander.write(hour_cnt_df)

with dwn5:
    st.download_button('Get Data', data=hour_cnt_df.to_csv().encode('utf-8'), file_name='by_hour.csv', mime='text/csv')   
