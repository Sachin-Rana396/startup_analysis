import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Funding')

df = pd.read_csv('startup_funding.csv')
df = df.drop(columns='Unnamed: 0')
df = df.set_index('Sr No')
# st.dataframe(df)
df['Date'] = pd.to_datetime(df.Date,errors='coerce')
df['Month'] = df.Date.dt.month
df['Year'] = df.Date.dt.year
 
# Sidebar
st.sidebar.title('Startup Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

# Overall Analysis
def load_overall_analysis():
    col1 , col2 ,col3,col4= st.columns(4)

    with col1:
        # Total Invested Amount
        total = round(df.Amount.sum())
        st.metric('Total',str(total) + ' Cr')
    with col2:
        # Maximum Investment on a Startup
        max_investment = df.groupby('Startup').Amount.sum().sort_values(ascending=False).head(1)
        st.metric('Max. Investment On a Startup',max_investment.index[0]+'=>'+str(round(max_investment.values[0])))
    with col3:
        # Mean Investment
        mean_investment = df.groupby('Startup').Amount.sum().mean()
        st.metric('Mean Investment',str(round(mean_investment)) + ' Cr')
    with col4:
        # Total Funded 
        total_funded = df['Startup'].nunique()
        st.metric('Total Funded Startup',str(total_funded) + ' Cr')
    
    # MoM Graph
    st.header('MoM Graph')
    temp_df_amount = df.groupby(['Year','Month']).Amount.sum().reset_index()
    temp_df_amount['x_axis'] = temp_df_amount['Month'].astype(str) + '-' + temp_df_amount['Year'].astype(str)

    temp_df_count = df.groupby(['Year','Month']).Startup.count().reset_index()
    temp_df_count['x_axis'] = temp_df_count['Month'].astype(str) + '-' + temp_df_count['Year'].astype(str)

    selected_option = st.selectbox('Select One',['Total Startup Funded','Total Amount Funded'])
    if selected_option =='Total Startup Funded':
        fig, ax = plt.subplots()
        ax.plot(temp_df_count['x_axis'],temp_df_count['Startup'])
        st.pyplot(fig)
    else:
        
        fig, ax = plt.subplots()
        ax.plot(temp_df_amount['x_axis'],temp_df_amount['Amount'])
        st.pyplot(fig)



round(df.Amount.sum())
# Investor page 
def load_investor_details(investor):
    st.title(investor)
    # Recent Investments
    st.subheader('Recent Investments')
    st.dataframe(df[df.Investors.str.contains(investor)].head()[['Date','Startup','Vertical','City','Type','Amount']])
    # Biggest Investments
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investments')
        big_series=df[df.Investors.str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    # Most Invested Sectors
    with col2:
        st.subheader('Most Invested Sectors')
        vertical_series = df[df.Investors.str.contains(investor)].head().groupby('Vertical')['Amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')

        st.pyplot(fig)
    col3, col4 = st.columns(2)
    # Investment Type
    with col3:
        st.subheader('Most Invested Sectors')
        vertical_series = df[df.Investors.str.contains(investor)].head().groupby('Type')['Amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')

        st.pyplot(fig)

    # City
    with col4:
        st.subheader('Cities')
        vertical_series = df[df.Investors.str.contains(investor)].head().groupby('City')['Amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')

        st.pyplot(fig)
    col5, col6 = st.columns(2)

    # YOY Investments
    with col5:
        df['Year'] = df['Date'].dt.year

        st.subheader('YoY Investments')
        investment_series = df[df.Investors.str.contains(investor)].groupby('Year')['Amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        ax.plot(investment_series.index,investment_series.values)

        st.pyplot(fig)
    


    
if option == 'Overall Analysis':
    st.title('Overall Analysis')
    load_overall_analysis()

elif option =='Startup':
    st.sidebar.selectbox('Select Startup',df['Startup'].drop_duplicates().to_list())
    btn1 = st.sidebar.button('Find Startup Details')

else:
    name = st.sidebar.selectbox('Select Investor',sorted(set(df.Investors.str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(name)