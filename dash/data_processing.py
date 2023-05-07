import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
HOT_df = pd.read_csv('C:/Users/mowus/Documents/GWU/youthmappers/YM_github/dash/base_data/HOT_data_may23.csv', parse_dates=['date'])
# print (HOT_df[0:5])

# ----------------------- Preprare data  -----------------------------------------------------------------------------------------------
# Assuming your data is stored in a Pandas DataFrame called df
HOT_df['date'] = pd.to_datetime(HOT_df['date'])  # Convert date column to datetime format
HOT_df['half_year'] = HOT_df['date'].dt.to_period('6M')  # Add new column with half-year periods

# Count the values in each half-year period
counts_by_half_year = HOT_df.groupby(['half_year', 'status']).count().reset_index()
print(counts_by_half_year)
# Convert Period to string
counts_by_half_year['half_year'] = counts_by_half_year['half_year'].astype(str)

# Plot
fig = px.line(counts_by_half_year, x=counts_by_half_year.half_year, y=counts_by_half_year.projectsID, title='Project Creation Time Series')
fig.show()


# ----------------------- Line graph -----------------------------------------------------------------------------------------------
fig = px.pie(counts_by_half_year, values=counts_by_half_year.projectsID, names='status', title='Overall status')
fig.show()