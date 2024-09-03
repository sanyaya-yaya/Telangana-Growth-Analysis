#!/usr/bin/env python
# coding: utf-8

# # Telangana growth analysis - Complete project

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[4]:


Transportation= pd.read_csv("fact_transport.csv")
Ipass=pd.read_csv("fact_TS_iPASS.csv")
Date=pd.read_csv("dim_date.csv")
stamp_registration=pd.read_csv("fact_stamps.csv")
district_names=pd.read_csv("dim_districts.csv")


# In[5]:


###Stamp Registration Analysis:

###1. District-wise Revenue Variation:

#Step 1: Calculate revenue for FY 2019 and FY 2022.

#Explanation: To calculate revenue for each year, you'll sum up the revenue generated from document registrations for each district in the respective fiscal year.


# In[6]:


district_names


# In[7]:


import pandas as pd

# Merge 'stamp_registration' with 'df2' based on the common column 'month'
merged_df = pd.merge(stamp_registration, 
                     Date, on='month', how='inner')

merged_df1 =pd.merge(merged_df, district_names, on='dist_code')
# Filter rows for FY 2019 and FY 2022
filtered_df = merged_df1[merged_df1['fiscal_year'].isin([2019, 2022])]

# Calculate revenue for FY 2019 and FY 2022
revenue_2019 = filtered_df[filtered_df['fiscal_year'] == 2019].groupby('dist_code')['documents_registered_rev'].sum()
revenue_2022 = filtered_df[filtered_df['fiscal_year'] == 2022].groupby('dist_code')['documents_registered_rev'].sum()

Total_revenue=pd.merge(revenue_2019,revenue_2022, on='dist_code')

Total_district_revenue=pd.merge(Total_revenue, district_names, on='dist_code')
Total_district_revenue.columns=['District_code', 'Documents_registered_rev_2019', 'Documents_registered_rev_2022',  'District']


# In[8]:


Total_district_revenue


# ### top 5 districts by revenue between 2019 and 2022, along with district names

# In[9]:


# Merging 'stamp_registration' with 'df2' using 'month' as the common column
combined_data = pd.merge(stamp_registration, Date, on='month')

# Filter data for fiscal years between 2019 and 2022
revenue_2019_to_2022 = combined_data[
    (combined_data['fiscal_year'] >= 2019) & (combined_data['fiscal_year'] <= 2022)
].groupby('dist_code')['documents_registered_rev'].sum()

# Sort the districts by revenue in descending order and get the top 5
top_5_districts = revenue_2019_to_2022.nlargest(5)

# Merge the top 5 districts with dim_districts to get district names
top_5_districts_with_highest_docsrevenue = pd.merge(top_5_districts.reset_index(),district_names, left_on='dist_code', right_on='dist_code')

# Now, top_5_districts_with_names will contain the top 5 districts by revenue between 2019 and 2022, along with district names.


# In[10]:


top_5_districts_with_highest_docsrevenue


# In[11]:


# Assuming 'stamp_registration' and 'df2' are your DataFrames, and 'month' is the common column
# Make sure to replace 'your_fiscal_year_column' with the actual column name for fiscal years in 'df2'

# Merge 'stamp_registration' with 'df2' using 'month' as the common column
combined_data = pd.merge(stamp_registration, Date, on='month')

# Filter data for fiscal years between 2019 and 2022
revenue_2019_to_2022 = combined_data[
    (combined_data['fiscal_year'] >= 2019) & (combined_data['fiscal_year'] <= 2022)
].groupby('dist_code')['estamps_challans_rev'].sum()

# Sort the districts by revenue in descending order and get the top 5
top_5_districts = revenue_2019_to_2022.nlargest(5)

# Merge the top 5 districts with dim_districts to get district names
top_5_districts_with_highest_estampsrevenue = pd.merge(top_5_districts.reset_index(),district_names, left_on='dist_code', right_on='dist_code')


# In[12]:


top_5_districts_with_highest_estampsrevenue


# ### top_5_contributing_e_stamp_districts_with_names will contain the top 5 districts where e-stamp revenue is significantly higher than document registration revenue in FY 2022, along with district names and revenue values

# In[13]:


# top_document_registration_districts and top_e_stamp_districts are the top districts for each revenue type

# Group by district and calculate total revenue for document registration in FY 2022
document_registration_revenue_2022 = combined_data.groupby('dist_code')['documents_registered_rev'].sum()

e_stamp_challan_2022 = combined_data[combined_data['fiscal_year'] == 2022]

# Group by district and calculate total e-stamp revenue in FY 2022
e_stamp_revenue_2022 = e_stamp_challan_2022.groupby('dist_code')['estamps_challans_rev'].sum()

# Calculate the difference between e-stamp revenue and document registration revenue in FY 2022
revenue_difference_2022 = e_stamp_revenue_2022 - document_registration_revenue_2022

# Sort the districts by revenue difference in descending order and get the top 5
top_5_contributing_e_stamp_districts = revenue_difference_2022.nlargest(5)

# Merge the top 5 contributing e-stamp districts with dim_districts to get district names and revenue values
top_5_contributing_e_stamp_districts_with_names = pd.merge(top_5_contributing_e_stamp_districts.reset_index(), district_names, left_on='dist_code', right_on='dist_code')


# In[15]:


top_5_contributing_e_stamp_districts_with_names


# In[14]:


# Filter data for FY 2022
stamp_registration_2022 = combined_data[combined_data['fiscal_year'] == 2022]
e_stamp_challan_2022 =combined_data[combined_data['fiscal_year'] == 2022]
e_stamp_challan_2021 =combined_data[combined_data['fiscal_year'] == 2021]
# Calculate total revenue for document registration in FY 2022 by district
document_registration_revenue_2022 = stamp_registration_2022.groupby('dist_code')['documents_registered_rev'].sum()

# Calculate total revenue for e-stamps in FY 2022 by district
e_stamp_revenue_2022 = e_stamp_challan_2022.groupby('dist_code')['estamps_challans_rev'].sum()
e_stamp_revenue_2021 = e_stamp_challan_2021.groupby('dist_code')['estamps_challans_rev'].sum()


# In[17]:


e_stamp_revenue_2021


# In[18]:


# Finding the top 5 districts with high revenue in document registration in FY 2022
top_5_document_registration_districts = document_registration_revenue_2022.nlargest(5)

# Finding the top 5 districts with high revenue in e-stamps in FY 2022
top_5_e_stamp_districts = e_stamp_revenue_2022.nlargest(5)


# In[19]:


top_5_document_registration_districts


# In[20]:


top_5_e_stamp_districts


# In[22]:


# Merging the top 5 document registration districts with dim_districts to get district names
top_5_document_registration_districts_with_names = pd.merge(top_5_document_registration_districts.reset_index(),district_names, left_on='dist_code', right_on='dist_code')

# Merging the top 5 e-stamp districts with dim_districts to get district names
top_5_e_stamp_districts_with_names = pd.merge(top_5_e_stamp_districts.reset_index(),district_names, left_on='dist_code', right_on='dist_code')


# In[23]:


top_5_document_registration_districts_with_names


# In[24]:


top_5_e_stamp_districts_with_names


# ### How does the revenue generated from document registration compare to the revenue generated from e-stamp challans across districts? List down the top 5 districts where e-stamps revenue contributes significantly more to the revenue than the documents in FY 2022

# In[25]:


# Compare the revenue values of e-stamps and document registration in 2022
higher_e_stamp_revenue_districts = e_stamp_revenue_2022[e_stamp_revenue_2022 > document_registration_revenue_2022]

# Merge the districts with dim_districts to get district names
higher_e_stamp_revenue_districts_with_names = pd.merge(higher_e_stamp_revenue_districts.reset_index(),district_names, left_on='dist_code', right_on='dist_code')


# In[26]:


# Sort the districts by e-stamp revenue in descending order and get the top 5
top_5_higher_e_stamp_revenue_districts = higher_e_stamp_revenue_districts_with_names.nlargest(5, 'estamps_challans_rev')

# Now, top_5_higher_e_stamp_revenue_districts will contain the top 5 districts where e-stamp revenue is higher than document registration revenue in 2022, along with district names and their respective revenue values.


# In[27]:


top_5_higher_e_stamp_revenue_districts


# In[28]:


# Merge the top 5 higher e-stamp revenue districts with their respective document registration values
top_5_higher_e_stamp_with_doc_registration = pd.merge(top_5_higher_e_stamp_revenue_districts, document_registration_revenue_2022.reset_index(), on='dist_code', suffixes=('_e_stamp', '_document_registration'))

# Rename columns for clarity
top_5_higher_e_stamp_with_doc_registration.rename(columns={'documents_registered_rev': 'document_registration_rev'}, inplace=True)

# Now, top_5_higher_e_stamp_with_doc_registration will contain the top 5 districts where e-stamp revenue is higher than document registration revenue in 2022, along with their respective e-stamp and document registration revenue values.


# In[29]:


top_5_higher_e_stamp_with_doc_registration


# ### Is there any alteration of e-Stamp challan count and document registration count pattern since the implementation of e-Stamp challan? If so, what suggestions would you propose to the government? 
#  
# 

# In[30]:


import matplotlib.pyplot as plt

# Create time-series plots with customization
plt.figure(figsize=(12, 6))
plt.plot(stamp_registration['month'], stamp_registration['estamps_challans_cnt'], label='E-Stamp Challan Counts', marker='o', linestyle='-', color='blue')
plt.plot(stamp_registration['month'],stamp_registration['documents_registered_cnt'], label='Document Registration Counts', marker='x', linestyle='--', color='green')
plt.xlabel('Month')
plt.ylabel('Counts')
plt.title('E-Stamp Challan Counts vs. Document Registration Counts Over Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Show the plot
plt.show()


# ### Categorize districts into three segments based on their stamp registration revenue generation during the fiscal year 2021 to 2022. 
#  
# 

# In[31]:


# Filter data for the fiscal year 2021 to 2022
revenue_2021_to_2022 = combined_data[
    (combined_data['fiscal_year'] >= 2021) & (combined_data['fiscal_year'] <= 2022)
]

# Calculate total stamp registration revenue by district
total_revenue_by_district = revenue_2021_to_2022.groupby('dist_code')['documents_registered_rev'].sum().reset_index()
total_revenue_by_district.rename(columns={'documents_registered_rev': 'total_revenue_2021_2022'}, inplace=True)



# In[32]:


total_revenue_by_district.head()


# In[33]:


# Calculating percentiles to define the segments
percentiles = total_revenue_by_district['total_revenue_2021_2022'].quantile([0, 0.33, 0.67, 1])

# Create categories based on percentiles
total_revenue_by_district['segment'] = pd.cut(
    total_revenue_by_district['total_revenue_2021_2022'],
    bins=percentiles,
    labels=['Low growth', 'Medium growth', 'High growth'],
    include_lowest=True
)


# In[34]:


total_revenue_by_district


# In[35]:


# Merging the district names with the categorization result
result_with_district_names = pd.merge(total_revenue_by_district, district_names, on='dist_code', how='left')

# The 'result_with_district_names' DataFrame now contains district names along with segments and total revenue.
# Define a custom sorting order for the 'segment' column
custom_sort_order = ['High growth', 'Medium growth', 'Low growth']

# Sort the DataFrame by the custom order
result_with_district_names['segment'] = pd.Categorical(result_with_district_names['segment'], categories=custom_sort_order, ordered=True)
result_with_district_names = result_with_district_names.sort_values(by='segment')

# Reset the index without adding a new index column
result_with_district_names.reset_index(drop=True, inplace=True)

# Now, the DataFrame is sorted with 'High' on top, 'Medium' in the middle, and 'Low' at the bottom.


# In[36]:


result_with_district_names


# # 2. Transportation
# 
# ### Step 1:Investigate whether there is any correlation between vehicle sales and specific months or seasons in different districts. Are there any months or seasons that consistently show higher or lower sales rate, and if yes, what could be the driving factors? (Consider Fuel-Type category only) 
# 

# In[37]:


Transportation= pd.read_csv("fact_transport.csv")
Ipass=pd.read_csv("fact_TS_iPASS.csv")
Date=pd.read_csv("dim_date.csv")
stamp_registration=pd.read_csv("fact_stamps.csv")
district_names=pd.read_csv("dim_districts.csv")


# In[38]:


Transportation.head()


# In[39]:


import pandas as pd

# Select relevant columns for the analysis
vehicle_sales_data = Transportation[['dist_code', 'month', 'fuel_type_petrol', 'fuel_type_diesel', 'fuel_type_electric', 'fuel_type_others',
                                    'vehicleClass_MotorCycle', 'vehicleClass_MotorCar', 'vehicleClass_AutoRickshaw', 'vehicleClass_Agriculture', 'vehicleClass_others',
                                    'seatCapacity_1_to_3', 'seatCapacity_4_to_6', 'seatCapacity_above_6', 'Brand_new_vehicles', 'Pre-owned_vehicles',
                                    'category_Non-Transport', 'category_Transport']]

# Convert 'month' to a datetime format
vehicle_sales_data['month'] = pd.to_datetime(vehicle_sales_data['month'])

# Extract month and year from the 'month' column
vehicle_sales_data['year'] = vehicle_sales_data['month'].dt.year
vehicle_sales_data['month'] = vehicle_sales_data['month'].dt.month

# Now, the 'vehicle_sales_data' DataFrame is prepared for analysis.


# In[40]:


vehicle_sales_data


# In[41]:


# Calculate the correlation between specific vehicle sales categories and 'month' (seasons)
correlation_petrol = vehicle_sales_data[['fuel_type_petrol', 'month']].corr().iloc[0, 1]
correlation_diesel = vehicle_sales_data[['fuel_type_diesel', 'month']].corr().iloc[0, 1]
correlation_electric = vehicle_sales_data[['fuel_type_electric', 'month']].corr().iloc[0, 1]
correlation_others = vehicle_sales_data[['fuel_type_others', 'month']].corr().iloc[0, 1]

# Repeat for other categories as needed

# Print the correlation values for each category
print(f"Correlation between petrol vehicle sales and month: {correlation_petrol}")
print(f"Correlation between diesel vehicle sales and month: {correlation_diesel}")
print(f"Correlation between electric vehicle sales and month: {correlation_electric}")
print(f"Correlation between others fuel type vehicle sales and month: {correlation_others}")
# Repeat for other categories as needed



# In[42]:


import matplotlib.pyplot as plt
import seaborn as sns

# Select the relevant columns for the analysis
fuel_types = ['fuel_type_petrol', 'fuel_type_diesel', 'fuel_type_electric', 'fuel_type_others']

# Create a bar chart for seasonal trends for each fuel type
plt.figure(figsize=(12, 6))

for fuel_type in fuel_types:
    # Group the data by month and calculate the mean sales for each month
    monthly_sales = vehicle_sales_data.groupby('month')[fuel_type].mean()
    
    # Create a bar chart for the current fuel type
    plt.bar(monthly_sales.index, monthly_sales, label=f'{fuel_type} Sales', alpha=0.7)

# Customize the plot
plt.xlabel('Month')
plt.ylabel('Average Sales')
plt.title('Seasonal Trends in Vehicle Sales by Fuel Type')
plt.legend()
plt.grid(False)

# Show the plot
plt.show()


# In[43]:


# import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Combine sales of all fuel types for each month
vehicle_sales_data['total_sales'] = vehicle_sales_data[fuel_types].sum(axis=1)

# Create a bar chart for the total seasonal trends
plt.figure(figsize=(12, 6))

# Group the data by month and calculate the total sales for each month
monthly_total_sales = vehicle_sales_data.groupby('month')['total_sales'].sum()

# Create a bar chart for the total sales
bars = plt.bar(monthly_total_sales.index, monthly_total_sales, label='Total Sales', alpha=0.7, color='blue')

# Customize the plot
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Total Seasonal Trends in Vehicle Sales')
plt.legend()

# Add exact value labels to the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}',
             ha='center', va='bottom', fontsize=8, color='black')

# Set x-axis ticks to ensure all months from January to December are displayed
all_months = [calendar.month_abbr[i] for i in range(1, 13)]  # Get month abbreviations
plt.xticks(range(1, 13), all_months)

# Remove grid lines
plt.grid(False)

# Show the plot
plt.show()


# ### How does the distribution of vehicles vary by vehicle class (MotorCycle, MotorCar, AutoRickshaw, Agriculture) across different districts? Are there any districts with a predominant preference for a specific vehicle class? Consider FY 2022 for analysis
# 
# 

# In[32]:


import pandas as pd

# Merge 'Transportation' and 'Date' DataFrames on the 'month' column
merged_data = pd.merge(Transportation, Date, on='month')


# Filter the merged data for FY 2022
merged_data_2022 = merged_data[merged_data['fiscal_year'] == 2022]

# Select the relevant columns for analysis
columns_of_interest = ['dist_code', 'vehicleClass_MotorCycle', 'vehicleClass_MotorCar', 'vehicleClass_AutoRickshaw', 'vehicleClass_Agriculture', 'vehicleClass_others']

# Group the data by district and calculate the total count of vehicles in each class for FY 2022
vehicle_distribution = merged_data_2022[columns_of_interest].groupby('dist_code').sum()

# Create a bar chart to visualize the distribution of vehicles by district and vehicle class
ax = vehicle_distribution.plot(kind='bar', stacked=True, figsize=(12, 6))

# Customize the plot
plt.xlabel('District Code')
plt.ylabel('Total Vehicle Count')
plt.title('Distribution of Vehicles by Vehicle Class (FY 2022)')
plt.legend(title='Vehicle Class')

# Show the plot
plt.show()


# In[35]:


import pandas as pd

# Merge 'Transportation' and 'Date' DataFrames on the 'month' column
merged_data = pd.merge(Transportation, Date, on='month')

# Merge the resulting DataFrame with 'district_names' on the 'dist_code' column
merged_data = pd.merge(merged_data, district_names, on='dist_code')

# Filter the merged data for FY 2022
merged_data_2022 = merged_data[merged_data['fiscal_year'] == 2022]

# Select the relevant columns for analysis
columns_of_interest = ['district', 'vehicleClass_MotorCycle', 'vehicleClass_MotorCar', 'vehicleClass_AutoRickshaw', 'vehicleClass_Agriculture', 'vehicleClass_others']

# Group the data by district and calculate the total count of vehicles in each class for FY 2022
vehicle_distribution = merged_data_2022[columns_of_interest].groupby('district').sum()

# Create a bar chart to visualize the distribution of vehicles by district and vehicle class
ax = vehicle_distribution.plot(kind='bar', stacked=True, figsize=(12, 6))

# Customize the plot
plt.xlabel('District Name')
plt.ylabel('Total Vehicle Count')
plt.title('Distribution of Vehicles by Vehicle Class (FY 2022)')
plt.legend(title='Vehicle Class')

# Show the plot
plt.show()


# In[46]:


district_names


# In[47]:


import pandas as pd
import matplotlib.pyplot as plt

# Merge 'Transportation' and 'Date' DataFrames on the 'month' column
merged_data = pd.merge(Transportation, Date, on='month')

# Filter the merged data for FY 2022
merged_data_2022 = merged_data[merged_data['fiscal_year'] == 2022]

# Select the relevant columns for analysis (excluding 'dist_code')
columns_of_interest = ['vehicleClass_MotorCycle', 'vehicleClass_MotorCar', 'vehicleClass_AutoRickshaw', 'vehicleClass_Agriculture', 'vehicleClass_others']

# Sum the counts of vehicles in each class for FY 2022
vehicle_distribution = merged_data_2022[columns_of_interest].sum()

# Create a pie chart to visualize the distribution of vehicles by vehicle class
fig, ax = plt.subplots(figsize=(8, 8))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
explode = (0.1, 0.1, 0.1, 0.1, 0.1)  # Explode the slices

# Plot the pie chart with additional styling
ax.pie(vehicle_distribution, labels=None, autopct='%1.1f%%', startangle=90, pctdistance=0.85,
       colors=colors, explode=explode, shadow=True)

# Customize the plot
plt.title('Distribution of Vehicles by Vehicle Class (FY 2022)')

# Create a legend with labels and color codes outside the chart
legend_labels = [f'{label} ({int(percentage)}%)' for label, percentage in zip(vehicle_distribution.index, vehicle_distribution / vehicle_distribution.sum() * 100)]
plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))



# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Show the plot
plt.show()


# In[58]:


vehicle_distribution


# ### List down the top 3 and bottom 3 districts that have shown the highest and lowest vehicle sales growth during FY 2022 compared to FY 2021? (Consider and compare categories: Petrol, Diesel and Electric) 

# In[48]:


import pandas as pd

# Merge 'Transportation' and 'Date' DataFrames on the 'month' column
Merged_Data = pd.merge(Transportation, Date, on='month')

# Filter the merged data for FY 2021 and FY 2022
DATA_2021 = Merged_Data[Merged_Data['fiscal_year'] == 2021]
DATA_2022= Merged_Data[Merged_Data['fiscal_year'] == 2022]

# Group the data by district and calculate the total vehicle sales for FY 2021 and FY 2022
Sales_2021 = DATA_2021.groupby('dist_code')['fuel_type_petrol', 'fuel_type_diesel', 'fuel_type_electric'].sum()
Sales_2022 = DATA_2022.groupby('dist_code')['fuel_type_petrol', 'fuel_type_diesel', 'fuel_type_electric'].sum()

# Merge the sales data with district names from 'district_names' DataFrame
Sales_2021 = pd.merge(district_names, Sales_2021, left_on='dist_code', right_index=True)
Sales_2022= pd.merge(district_names, Sales_2022, left_on='dist_code', right_index=True)

# Rename the columns for clarity
Sales_2021.columns = ['Dist_Code', 'District', 'petrol_sales_2021', 'diesel_sales_2021', 'electric_sales_2021']
Sales_2022.columns = ['Dist_Code', 'District', 'petrol_sales_2022', 'diesel_sales_2022', 'electric_sales_2022']

# Find the top 3 and bottom 3 districts for FY 2021 based on total sales
top_3_2021 = Sales_2021.nlargest(3, 'petrol_sales_2021')
bottom_3_2021 = Sales_2021.nsmallest(3, 'petrol_sales_2021')

# Find the top 3 and bottom 3 districts for FY 2022 based on total sales
top_3_2022 = Sales_2022.nlargest(3, 'petrol_sales_2022')
bottom_3_2022 = Sales_2022.nsmallest(3, 'petrol_sales_2022')

# Display the results
print("Top 3 Districts for FY 2021 based on Petrol Sales:")
print(top_3_2021[['District', 'petrol_sales_2021']])

print("\nBottom 3 Districts for FY 2021 based on Petrol Sales:")
print(bottom_3_2021[['District', 'petrol_sales_2021']])

print("\nTop 3 Districts for FY 2022 based on Petrol Sales:")
print(top_3_2022[['District', 'petrol_sales_2022']])

print("\nBottom 3 Districts for FY 2022 based on Petrol Sales:")
print(bottom_3_2022[['District', 'petrol_sales_2022']])


# In[49]:


# Create a figure with subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(13, 12))
fig.subplots_adjust(wspace=0.4, hspace=0.5)

# Define colors for bars
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Plot top 3 districts for FY 2021 based on Petrol Sales
axes[0, 0].bar(top_3_2021['District'], top_3_2021['petrol_sales_2021'], color=bar_colors)
axes[0, 0].set_title('Top 3 Districts for FY 2021 (Petrol Sales)')
axes[0, 0].set_ylabel('Petrol Sales')

# Plot bottom 3 districts for FY 2021 based on Petrol Sales
axes[0, 1].bar(bottom_3_2021['District'], bottom_3_2021['petrol_sales_2021'], color=bar_colors)
axes[0, 1].set_title('Bottom 3 Districts for FY 2021 (Petrol Sales)')
axes[0, 1].set_ylabel('Petrol Sales')

# Plot top 3 districts for FY 2022 based on Petrol Sales
axes[1, 0].bar(top_3_2022['District'], top_3_2022['petrol_sales_2022'], color=bar_colors)
axes[1, 0].set_title('Top 3 Districts for FY 2022 (Petrol Sales)')
axes[1, 0].set_ylabel('Petrol Sales')

# Plot bottom 3 districts for FY 2022 based on Petrol Sales
axes[1, 1].bar(bottom_3_2022['District'], bottom_3_2022['petrol_sales_2022'], color=bar_colors)
axes[1, 1].set_title('Bottom 3 Districts for FY 2022 (Petrol Sales)')
axes[1, 1].set_ylabel('Petrol Sales')

# Rotate x-axis labels for better readability
for ax in axes.flatten():
    ax.tick_params(axis='x', rotation=0)

# Add grid lines
for ax in axes.flatten():
    ax.grid(False)

# Add value labels above bars
for ax in axes.flatten():
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 3., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                    textcoords='offset points')

# Adjust layout and show the plot
plt.tight_layout()
plt.show()


# ## Ts-Ipass (Telangana State Industrial Project Approval and Self Certification System) 
# ### List down the top 5 sectors that have witnessed the most significant investments in FY 2022. 
# 

# In[6]:


Ipass.head()


# In[7]:


import pandas as pd

# Standardize the date format in the 'month' column of 'TS-iPASS' dataset
Ipass['month'] = pd.to_datetime(Ipass['month'], format='%d-%m-%Y')

# Standardize the date format in the 'month' column of 'Date' dataset
Date['month'] = pd.to_datetime(Date['month'])

# Merge the datasets based on the 'month' column
merged_data = pd.merge(Ipass, Date, on='month')

# Now, both datasets should have the same date format and data type for the 'month' column


# In[8]:


merged_data


# In[9]:


import pandas as pd
ts_ipass_merged = pd.merge(Ipass, Date, on='month')
fy_2022_data = ts_ipass_merged[ts_ipass_merged['fiscal_year'] == 2022]

# Group the data by sector and calculate total investment
sector_investment_2022 = fy_2022_data.groupby('sector')['investment in cr'].sum()

# Sort sectors by total investment in descending order and select the top 5
top_5_sectors_2022 = sector_investment_2022.nlargest(5)

# Display the top 5 sectors
print("Top 5 Sectors with the Most Significant Investments in FY 2022:")
print(top_5_sectors_2022)


# In[10]:


import matplotlib.pyplot as plt

# Assuming you have the 'top_5_sectors_2022' Series from the previous code

# Define custom colors
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(top_5_sectors_2022, labels=top_5_sectors_2022.index, autopct='%1.1f%%', startangle=140, colors=colors)

# Add a title
plt.title("Top 5 Sectors with the Most Significant Investments in FY 2022")

# Create a legend box with color codes and values
legend_labels = [f'{sector}: {investment:.2f} Cr' for sector, investment in zip(top_5_sectors_2022.index, top_5_sectors_2022)]
plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1.5, 0.5))

# Display values inside the pie chart
plt.gca().set_aspect("equal")


# Show the pie chart
plt.show()


# ### List down the top 3 districts that have attracted the most significant sector investments during FY 2019 to 2022? What factors could have led to the substantial investments in these particular districts? 

# In[11]:


# import pandas as pd
# Filter the data for FY 2019 to 2022
data_2019_2022 = merged_data[(merged_data['fiscal_year'] >= 2019) & (merged_data['fiscal_year'] <= 2022)]

# Group the data by district and calculate the total sector investments
district_sector_investments = data_2019_2022.groupby('dist_code')['investment in cr'].sum()

# Merge the investments data with district names from 'district_names_df'
district_investments_with_names = pd.merge(district_names, district_sector_investments, left_on='dist_code', right_index=True)

# Find the top 3 districts with the most significant sector investments
top_3_districts_investments = district_investments_with_names.nlargest(3, 'investment in cr')

# Display the top 3 districts and their sector investments
print("Top 3 Districts with the Most Significant Sector Investments (FY 2019 to 2022):")
print(top_3_districts_investments)


# In[12]:


import pandas as pd
import matplotlib.pyplot as plt

# Filter the data for FY 2019 to 2022
data_2019_2022 = merged_data[(merged_data['fiscal_year'] >= 2019) & (merged_data['fiscal_year'] <= 2022)]

# Group the data by district and calculate the total sector investments
district_sector_investments = data_2019_2022.groupby('dist_code')['investment in cr'].sum()

# Merge the investments data with district names from 'district_names_df'
district_investments_with_names = pd.merge(district_names, district_sector_investments, left_on='dist_code', right_index=True)

# Find the top 3 districts with the most significant sector investments
top_3_districts_investments = district_investments_with_names.nlargest(3, 'investment in cr')

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_3_districts_investments['district'], top_3_districts_investments['investment in cr'], color='LightGreen')
plt.xlabel('Districts')
plt.ylabel('Total Investment (in Crores)')
plt.title('Top 3 Districts with the Most Significant Sector Investments (FY 2019 to 2022)')

# Rotate x-axis labels for better readability
plt.xticks(rotation=0)

# Display the values on top of the bars
for i, v in enumerate(top_3_districts_investments['investment in cr']):
    plt.text(i, v, f'{v:.2f} Cr', ha='center', va='bottom')

# Show the bar chart
plt.tight_layout()
plt.show()


# ### Is there any relationship between district investments, vehicles sales and stamps revenue within the same district between FY 2021 and 2022? 
#  
# 

# In[16]:


import pandas as pd

# Merge 'Tpass1' and 'Transportation' DataFrames on 'dist_code' and 'month' columns
Ipass['month'] = pd.to_datetime(Ipass['month'], format='%d-%m-%Y')
Transportation['month'] = pd.to_datetime(Transportation['month'], format='%Y-%m-%d')

merged_data = pd.merge(Ipass, Transportation, on=['dist_code', 'month'])

# Merge 'merged_data' and 'Date' DataFrames on 'month' column
merged_data4 = pd.merge(merged_data, Date, on='month')

merged_data5 = pd.merge(merged_data4, stamp_registration, on='dist_code')
# Filter the merged data for FY 2021 and FY 2022
data_2021_2022 = merged_data5[(merged_data5['fiscal_year'] >= 2021) & (merged_data5['fiscal_year'] <= 2022)]

# Group the data by district and calculate the total investments, vehicle sales, and stamp revenue for FY 2021 and FY 2022
total_investments_2021_2022 = data_2021_2022.groupby('dist_code')['investment in cr'].sum()

total_vehicle_sales_2021_2022 = data_2021_2022.groupby('dist_code')[
    'fuel_type_petrol', 'fuel_type_diesel', 'fuel_type_electric'
].sum()

total_stamps_revenue_2021_2022 = data_2021_2022.groupby('dist_code')['estamps_challans_rev'].sum()


# Merge the results with district names from 'D_names' DataFrame
total_investments_2021_2022 = pd.merge(district_names, total_investments_2021_2022, left_on='dist_code', right_index=True)


total_vehicle_sales_2021_2022 = pd.merge(district_names, total_vehicle_sales_2021_2022, left_on='dist_code', right_index=True)


total_stamps_revenue_2021_2022 = pd.merge(district_names, total_stamps_revenue_2021_2022, left_on='dist_code', right_index=True)

# Merge investments and vehicle sales on 'district'
merged6 = pd.merge(total_investments_2021_2022, total_vehicle_sales_2021_2022, on='district')

# Merge the above result with stamps revenue on 'district'
final = pd.merge(merged6, total_stamps_revenue_2021_2022, on='district')

print(final)


# ### 11.	Are there any particular sectors that have shown substantial investment in multiple districts between FY 2021 and 2022? 

# In[25]:


import pandas as pd

# Merge 'Ipass1' and 'Date' DataFrames on the 'month' column
Ipass1 = pd.merge(Ipass, Date, on='month')
Ipass3 = pd.merge(Ipass1, district_names, on ='dist_code')
# Filter 'Ipass' dataset for FY 2021 and FY 2022
ipass_2021 = Ipass3[Ipass3['fiscal_year'] == 2021]
ipass_2022 = Ipass3[Ipass3['fiscal_year'] == 2022]

# Group and sum total investments by sector and district for both years
investment_2021 = ipass_2021.groupby(['sector', 'dist_code'])['investment in cr'].sum().reset_index()
investment_2022 = ipass_2022.groupby(['sector', 'dist_code'])['investment in cr'].sum().reset_index()

# Sum total investments across districts for each sector in both years
total_investment_2021 = investment_2021.groupby('sector')['investment in cr'].sum().reset_index()
total_investment_2022 = investment_2022.groupby('sector')['investment in cr'].sum().reset_index()

# Merge the total investments for both years
investment_comparison = pd.merge(total_investment_2021, total_investment_2022, on='sector', suffixes=('_2021', '_2022'))

# Define a threshold for substantial investment growth (you can adjust this threshold as needed)
threshold = 100  # Example threshold, adjust as per your analysis criteria

# Filter sectors with substantial investment growth
substantial_investment_growth = investment_comparison[investment_comparison['investment in cr_2022'] > threshold]

# Count the number of districts with investments for each sector
district_count = investment_2022.groupby('sector')['dist_code'].count().reset_index()

# Merge the district count with the substantial investment growth data
substantial_investment_growth = pd.merge(substantial_investment_growth, district_count, on='sector', how='left')

# Rename the columns for clarity
substantial_investment_growth.rename(columns={'dist_code': 'no of districts'}, inplace=True)

# Sort the sectors by the number of districts in descending order
substantial_investment_growth = substantial_investment_growth.sort_values(by='no of districts', ascending=False)

# Display the sorted results
print("Sectors with Substantial Investment in Multiple Districts between FY 2021 and 2022 (Sorted by District Count):")
print(substantial_investment_growth[['sector', 'investment in cr_2022', 'no of districts']])


# In[22]:


import pandas as pd
import matplotlib.pyplot as plt

# Sort the sectors by the number of districts in descending order
substantial_investment_growth = substantial_investment_growth.sort_values(by='no of districts', ascending=False)

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.barh(substantial_investment_growth['sector'], substantial_investment_growth['no of districts'], color='skyblue')
plt.xlabel('Number of Districts')
plt.ylabel('Sector')
plt.title('Sectors with Substantial Investment in Multiple Districts (Sorted by District Count)')
plt.gca().invert_yaxis()  # Invert the y-axis to display the highest count at the top

# Display the chart
plt.show()


# #### Can we identify any seasonal patterns or cyclicality in the investment trends for specific sectors? Do certain sectors              experience higher investments during particular months? 
# 

# In[26]:


import pandas as pd
import matplotlib.pyplot as plt

# Convert the 'month' column to datetime if it's not already
Ipass1['month'] = pd.to_datetime(Ipass1['month'])

# Sort the data by month
investment_data = Ipass1.sort_values(by=['sector', 'month'])

# Get a list of unique sectors in the dataset
unique_sectors = investment_data['sector'].unique()

# Create a line plot for each sector in separate subplots
plt.figure(figsize=(12, 6 * len(unique_sectors)))

for i, sector in enumerate(unique_sectors, 1):
    sector_data = investment_data[investment_data['sector'] == sector]
    
    plt.subplot(len(unique_sectors), 1, i)
    plt.plot(sector_data['month'], sector_data['investment in cr'])
    plt.xlabel('Month')
    plt.ylabel('Investment in Crores')
    plt.title(f'Investment Trends for Sector: {sector}')
    plt.grid(True)
    
    # Customize the x-axis labels to show months
    plt.xticks(rotation=45)

# Adjust spacing between subplots
plt.tight_layout()

# Display the individual line plots for each sector
plt.show()


# # Secondary research 

# ### The top 5 districts to buy commercial properties in Telangana.

# In[27]:


import pandas as pd

# Group the data by district and calculate the total revenue from documents registered
district_revenue = stamp_registration.groupby('dist_code')['documents_registered_rev'].sum()

# Sort the districts by revenue in descending order
top_5_districts = district_revenue.nlargest(5)

# Print the top 5 districts for commercial property investments
print("Top 5 Districts to Buy Commercial Properties in Telangana:")
print(top_5_districts)


# In[28]:


import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have the 'stamp_registration_data' DataFrame with columns: 'dist_code', 'documents_registered_rev'

# Group the data by district and calculate the total revenue from documents registered
district_revenue = stamp_registration.groupby('dist_code')['documents_registered_rev'].sum()

# Sort the districts by revenue in descending order and select the top 5
top_5_districts = district_revenue.nlargest(5)

# Get district names for the top 5 districts (assuming you have a 'district_names' DataFrame)
top_5_district_names = district_names[district_names['dist_code'].isin(top_5_districts.index)]['district']

# Define custom colors for the bars
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Create a bar plot with custom styling
plt.figure(figsize=(10, 6))
bars = plt.bar(top_5_district_names, top_5_districts, color=colors)
plt.xlabel('Districts')
plt.ylabel('Total Revenue (in Crores)')
plt.title('Top 5 Districts to Buy Commercial Properties in Telangana')
plt.xticks(rotation=0)

# Add data labels above the bars
for bar, revenue in zip(bars, top_5_districts):
    plt.text(bar.get_x() + bar.get_width() / 2, revenue + 0.5, f'{revenue:.2f} Cr', ha='center', va='bottom')

# Add a grid for better readability
plt.grid(False)

# Show the plot
plt.tight_layout()
plt.show()


# # Completed
