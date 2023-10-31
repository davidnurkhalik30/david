import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Helper function
def create_daily_rentals_df(all_df):
    daily_rentals_df = all_df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "instant": "bike rentals",
    }, inplace=True)
    
    return daily_rentals_df

def create_bygrowthperyear_df(all_df):
    bygrowthperyear_df = all_df.groupby(by="yr").instant.nunique().reset_index()
    bygrowthperyear_df.rename(columns={
        "instant": "bike rental"
    }, inplace=True)
    
    return bygrowthperyear_df

def create_byseason_df(all_df):
    byseason_df = all_df.groupby(by="season").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "bike rental"
    }, inplace=True)
    
    return byseason_df

def create_bymonth_df(all_df):
    bymonth_df = all_df.groupby(by="mnth").instant.nunique().reset_index()
    bymonth_df.rename(columns={
        "instant": "bike rental"
    }, inplace=True)
    
    return bymonth_df

def create_byweekday_df(all_df):
    byweekday_df = all_df.groupby(by="weekday").instant.nunique().reset_index()
    byweekday_df.rename(columns={
        "instant": "bike rental"
    }, inplace=True)
    
    return byweekday_df

def create_byworkingday_df(all_df):
    byworkingday_df = all_df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_df.rename(columns={
        "instant": "bike rental"
    }, inplace=True)
    
    return byworkingday_df

# Load cleaned data
all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday", "dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image('bike.jpg')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


# st.dataframe(main_df)
# # Menyiapkan berbagai dataframe
daily_rentals_df = create_daily_rentals_df(main_df)
bygrowthperyear_df = create_bygrowthperyear_df(main_df)
byseason_df = create_byseason_df(main_df)
bymonth_df = create_bymonth_df(main_df)
byweekday_df = create_byweekday_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)

# plot number of daily orders (2021)
st.header('Bike Rental Dashboard In Hours :fire:')

st.subheader('Daily Bike Rentals')
 
col1, col2 , col3= st.columns(3)
 
with col1:
    total_rental = main_df.instant.sum()
    st.metric("Rentals User", value=total_rental)
 
with col2:
    total_casual = main_df.casual.sum() 
    st.metric("Casual User", value=total_casual)

with col3:
    total_registered = main_df.registered.sum()
    st.metric("Registered User", value=total_registered)

#bygrowthperyear_df 
st.subheader('Growth Per Year')
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x=bygrowthperyear_df["bike rental"],
    y=bygrowthperyear_df["yr"],
    marker='o', 
    linewidth=10,
    color="#90CAF9",
    ax=ax
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# byseason
st.subheader("Seasonly Rentals in Hours")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="bike rental", 
    x="season"  ,
    data=byseason_df.sort_values(by="bike rental", ascending=False),
    ax=ax
)
ax.set_title("Number of Bike Rental by Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#bymonth
st.subheader("Monthly Rentals in Hours")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="bike rental", 
    x="mnth"  ,
    data=bymonth_df.sort_values(by="bike rental", ascending=False),
    ax=ax
)
ax.set_title("Number of Bike Rental by Month", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#byweekday
st.subheader("Weekday Rental in Hours")
fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y="bike rental", 
    x="weekday",
    data=byweekday_df.sort_values(by="bike rental", ascending=False),
    ax=ax
)
ax.set_title("Number of Bike Rental by Weekday", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#byworkingday
st.subheader("Workingday Rental in Hours")
fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y="bike rental", 
    x="workingday",
    data=byworkingday_df.sort_values(by="bike rental", ascending=False),
    ax=ax
)
ax.set_title("Number of Bike Rental by Workingday", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


st.caption('Copyright © David Nurkhalik 2023')


