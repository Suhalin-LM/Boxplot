import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
file_path = 'Open Transaction Data.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet 1')

# Data cleaning: Ensure 'Transaction Price' is numeric
df['Transaction Price'] = pd.to_numeric(df['Transaction Price'], errors='coerce')

# Streamlit app
st.title('Boxplot of Transaction Prices by Property Type and District')

# Page navigation
page = st.sidebar.radio("Navigation", ["District Selection", "Boxplot Visualization"])

if page == "District Selection":
    st.header("Step 1: Select Districts")
    # Use checkboxes for district selection
    districts = df['District'].unique()
    selected_districts = []

    with st.form("district_selection_form"):
        for district in districts:
            if st.checkbox(district, key=district):
                selected_districts.append(district)

        submit_button = st.form_submit_button("Confirm Selection")

    # Store selected districts in session state
    st.session_state["selected_districts"] = selected_districts

    st.write("You have selected the following districts:", selected_districts)

elif page == "Boxplot Visualization":
    st.header("Step 2: Visualize Boxplot")
    
    # Retrieve selected districts from session state
    selected_districts = st.session_state.get("selected_districts", [])

    if selected_districts:
        # Filter data based on selected districts
        df = df[df['District'].isin(selected_districts)]

        # Sidebar filters for Property Types
        if st.sidebar.button('Select All Property Types'):
            selected_property_types = df['Property Type'].unique()
        elif st.sidebar.button('Unselect All Property Types'):
            selected_property_types = []
        else:
            selected_property_types = st.sidebar.multiselect('Select Property Type(s)', options=df['Property Type'].unique(), default=df['Property Type'].unique())

        # Filter data based on selection
        filtered_data = df[df['Property Type'].isin(selected_property_types)]

        # Check if there is data to plot
        if not filtered_data.empty:
            # Create boxplot
            st.write('### Boxplot of Transaction Prices')
            plt.figure(figsize=(12, 6))
            sns.boxplot(data=filtered_data, x='District', y='Transaction Price', hue='Property Type')
            plt.xticks(rotation=45)
            plt.title('Transaction Prices by Property Type and District')
            plt.ylabel('Transaction Price')
            plt.xlabel('District')
            st.pyplot(plt)

            # General explanation of the boxplot
            st.write("Transaction Price (RM in Million)")
            st.write("### Observations from the Boxplot")
            st.write("The boxplot provides a visual representation of the transaction prices for different property types across selected districts. Key observations include:")
            st.write("- The spread of transaction prices (range between the minimum and maximum values) for each district and property type.")
            st.write("- The median transaction price for each category, represented by the horizontal line within each box.")
            st.write("- Any outliers, which are shown as individual points outside the whiskers of the boxplot.")
            st.write("- Differences in price distributions between property types within the same district.")
        else:
            st.write('No data available for the selected filters.')
    else:
        st.write("Please select at least one district in the 'District Selection' page.")
