import pandas as pd
import plotly.express as px
import streamlit as st 

st.set_page_config(
    page_title= "Sales Dashboard",
    page_icon= "bar_chart:",
    layout="wide"
)

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io = "supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols='B:R',
        nrows= 1000
    )
    # add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

st.dataframe(df)
# Sidebar 
st.sidebar.header("Please Filter Here :")
city  = st.sidebar.multiselect(
    "Select The City :",
    options = df["City"].unique(),
    default = df["City"].unique()
)
Customer_type = st.sidebar.multiselect(
    "Select The Customer_type :",
    options = df["Customer_type"].unique(),
    default = df["Customer_type"].unique()
)
gender  = st.sidebar.multiselect(
    "Select The Gender :",
    options = df["Gender"].unique(),
    default = df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @Customer_type & Gender == @gender  "
)


# MainPage
st.title(':bar_chart: Sales Dashboard')
st.markdown("##")

# Top KPI's 
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating , 0))
average_sales_by_transaction = round(df_selection["Total"].mean(),2)

left_column , middel_column , rigth_column = st.columns(3)
with left_column:
    st.subheader("Total Sales : ")
    st.subheader(f"US $ {total_sales:,}")

with middel_column:
    st.subheader("Average Rating : ")
    st.subheader(f"{average_rating} {star_rating}")

with rigth_column:
    st.subheader("Average Sales By Transactions: ")
    st.subheader(f"US $ {average_sales_by_transaction}")

st.markdown("---")


# Sales By Product Line [bar_chart]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by='Total')
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b> Sales by Product Line </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid = False))
)


# Sales by hour [bar chart]
sales_by_hour = (
    df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]
)

fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b> Sales by Hour </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)
fig_hourly_sales.update_layout(
    xaxis = (dict(tickmode = "linear")),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid = False))
)

left_column , rigth_column = st.columns(2)
left_column.plotly_chart(fig_product_sales,use_container_width=True)
rigth_column.plotly_chart(fig_hourly_sales,use_container_width=True)
