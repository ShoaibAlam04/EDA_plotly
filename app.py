import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")


df = pd.read_csv("C:\\Users\\LENOVO\\Downloads\\online_retail.csv")


df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M')

date_range = st.date_input("Select Date Range", [df['InvoiceDate'].min(), df['InvoiceDate'].max()], format="YYYY-MM-DD")


start_date, end_date = pd.to_datetime(date_range, errors='coerce')

# Filter data based on selected date range, positive quantity & unit price
filtered_df = df[(df['InvoiceDate'] >= start_date) & (df['InvoiceDate'] <= end_date) &
                 (df['Quantity'] >= 0) & (df['UnitPrice'] > 0)]

# Display data overview
st.title("Online Retail Analysis Dashboard")
st.subheader("Data Overview")
st.dataframe(filtered_df.head())

# Count of null and non-null CustomerID
non_null_count = len(filtered_df.dropna(subset=['CustomerID']))
null_count = df['CustomerID'].isnull().sum()

colors = ['#FF9999', '#66B2FF']

fig_null_count = go.Figure(data=[
    go.Bar(x=['Non-Null CustomerID', 'Null CustomerID'], y=[non_null_count, null_count], marker_color=colors)
])

fig_null_count.update_layout(
    title='Count of Null and Non-Null CustomerID',
    title_x=0.5,  # Center title
    yaxis_title='Count'
)
st.plotly_chart(fig_null_count)

filtered_df = filtered_df.dropna(subset=['CustomerID'])
filtered_df_description = filtered_df.describe()

# Display the DataFrame description in Streamlit
st.dataframe(filtered_df_description)

col1, col2 = st.columns(2)

# Quantity by Country (Bar Chart)
bar_chart = filtered_df.groupby('Country')['Quantity'].sum().reset_index()
fig = go.Figure(data=[go.Bar(x=bar_chart['Country'], y=bar_chart['Quantity'], marker_color='green')])
fig.update_layout(title='Quantity by Country', xaxis_title='Country', yaxis_title='Quantity',
                  height=400, width=400, title_x=0.5)  # Center title
col1.plotly_chart(fig)

# Scatter Plot: InvoiceDate vs. UnitPrice
scatter_plot = filtered_df.sample(1000)
scatter_fig = px.scatter(scatter_plot, x='InvoiceDate', y='UnitPrice', color='Quantity',
                         size='Quantity', opacity=0.7, template='plotly_dark',
                         title='InvoiceDate vs. UnitPrice')
scatter_fig.update_layout(title_x=0.5)  # Center title
col2.plotly_chart(scatter_fig)






# Top 10 Items by Quantity
col3, col4 = st.columns(2)



top_10_items = filtered_df.groupby('StockCode')['Quantity'].sum().nlargest(10).reset_index()
colors = px.colors.qualitative.Set3[:10]


fig_top_items = go.Figure(data=[
    go.Bar(x=top_10_items['StockCode'], y=top_10_items['Quantity'],
           text=top_10_items['Quantity'], marker_color=colors)
])


fig_top_items.update_layout(
    title='Top 10 Items by Quantity',
    title_x=0.5,
    xaxis_title='StockCode',
    yaxis_title='Total Quantity'
)

col3.plotly_chart(fig_top_items)


# StockCode Distribution
pie_chart = df['StockCode'].value_counts().reset_index()
fig4 = go.Figure(go.Pie(labels=pie_chart['StockCode'], values=pie_chart['StockCode']))
fig4.update_layout(title='Distribution of StockCode', height=400, width=400)
col4.plotly_chart(fig4)


col5, col6 = st.columns(2)

# 3D Scatter Plot: Quantity vs. UnitPrice vs. Country
country_codes = {country: code for code, country in enumerate(filtered_df['Country'].unique())}
filtered_df['CountryCode'] = filtered_df['Country'].map(country_codes)

fig_3d_scatter = go.Figure(data=[
    go.Scatter3d(
        x=filtered_df['Quantity'],
        y=filtered_df['UnitPrice'],
        z=filtered_df['CountryCode'],
        mode='markers',
        text=filtered_df[['Quantity', 'UnitPrice', 'Country']],
        marker=dict(
            size=5,
            color=filtered_df['CountryCode'],  
            opacity=0.7,
            colorscale='Viridis'
        )
    )
])


fig_3d_scatter.update_layout(
    title='Quantity vs. UnitPrice vs. Country',
    title_x=0.5,
    scene=dict(
        xaxis_title='Quantity',
        yaxis_title='UnitPrice',
        zaxis_title='Country'
    )
)

col5.plotly_chart(fig_3d_scatter)







# Top 10 Customers by Number of Transactions
transactions_per_customer = filtered_df['CustomerID'].astype(str).value_counts().head(10).reset_index()
transactions_per_customer.columns = ['CustomerID', 'NumberOfTransactions']


colors = ['rgb(255, 87, 34)', 'rgb(63, 81, 181)', 'rgb(76, 175, 80)', 'rgb(255, 193, 7)',
          'rgb(233, 30, 99)', 'rgb(33, 150, 243)', 'rgb(255, 152, 0)', 'rgb(156, 39, 176)',
          'rgb(0, 150, 136)', 'rgb(103, 58, 183)']


fig_top_customers = go.Figure(data=[
    go.Bar(
        x=transactions_per_customer['CustomerID'],
        y=transactions_per_customer['NumberOfTransactions'],
        marker=dict(color=colors)
    )
])


fig_top_customers.update_layout(
    title='Top 10 Customers by Number of Transactions',
    title_x=0.5, 
    xaxis=dict(
        tickmode='array',
        tickvals=transactions_per_customer['CustomerID'].tolist(),
        ticktext=transactions_per_customer['CustomerID'].tolist(),
        title='Customer ID'
    ),
    yaxis=dict(title='Number of Transactions'),
    barmode='group',  
    bargap=0.4,  
    bargroupgap=0.4  
)


col6.plotly_chart(fig_top_customers)
