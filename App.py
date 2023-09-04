import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt

def calculate_super_pixel_metrics(Monthly_Traffic, Cost_Per_Acquisition, Sales_Conversion_Rate, Deal_Value, Re_opt_in_percent, Re_activation_Sales_Rate, Cost_Per_Match_Reactivation, Verification_percent, ID_Resolution_Match_percent):
    if (Monthly_Traffic > 0 and Cost_Per_Acquisition > 0 and 0 <= Sales_Conversion_Rate <= 1.0
        and Deal_Value > 0 and 0 <= Re_opt_in_percent <= 1.0
        and 0 <= Re_activation_Sales_Rate <= 1.0
        and Cost_Per_Match_Reactivation >= 0 and 0 <= Verification_percent <= 1.0
        and 0 <= ID_Resolution_Match_percent <= 1.0):
        Sales = Monthly_Traffic * Sales_Conversion_Rate
        Revenue = Sales * Deal_Value
        Estimated_Spend = Sales * Cost_Per_Acquisition
        Anonymous_Traffic = Monthly_Traffic - (Monthly_Traffic * Sales_Conversion_Rate)
        Consumer_Matches = Anonymous_Traffic * ID_Resolution_Match_percent
        Verified_Matched_Profiles = Consumer_Matches * Verification_percent
        Recovered_Leads = Verified_Matched_Profiles * Re_opt_in_percent
        Recovered_Sales = Recovered_Leads * Re_activation_Sales_Rate
        Recovered_Revenue = Recovered_Sales * Deal_Value
        Total = Cost_Per_Match_Reactivation * Recovered_Leads
        CPA_After = Total / Recovered_Sales
        calculated_values = {
            "Sales": Sales,
            "Revenue": Revenue,
            "Estimated Spend": Estimated_Spend,
            "Anonymous Traffic": int(Anonymous_Traffic),
            "Consumer Matches": int(Consumer_Matches),
            "Verified Matched_Profiles": int(Verified_Matched_Profiles),
            "Recovered Leads": int(Recovered_Leads),
            "Recovered Sales": Recovered_Sales,
            "Recovered Revenue": Recovered_Revenue,
            "Total": Total,
            "CPA(After)": CPA_After
        }
    else:
        calculated_values = {}  # Return an empty dictionary if conditions are not satisfied
    return calculated_values

def main():
    st.set_page_config(page_title="SuperPixel Calculator By Debby", layout="wide", initial_sidebar_state='expanded')
    
    st.markdown("<h1 style='text-align: center; margin-top: 1em;'>SuperPixel Calculator by Debby</h1>", unsafe_allow_html=True)
    
    st.sidebar.markdown("### Input Parameters")
    st.sidebar.markdown("---")

    Monthly_Traffic = st.sidebar.number_input("Monthly Traffic:", min_value=0)
    Cost_Per_Acquisition = st.sidebar.number_input("Cost Per Acquisition:", min_value=0)
    Sales_Conversion_Rate = st.sidebar.number_input("Sales Conversion Rate:", min_value=0.0, max_value=1.0, step=0.01)
    Deal_Value = st.sidebar.number_input("Deal Value:", min_value=0)
    Re_opt_in_percent = st.sidebar.number_input("Re-Opt-in Percent:", min_value=0.0, max_value=1.0, step=0.01)
    Re_activation_Sales_Rate = st.sidebar.number_input("Re-Activation Sales Rate:", min_value=0.0, max_value=1.0, step=0.01)
    Cost_Per_Match_Reactivation = st.sidebar.number_input("Cost Per Match Re-Activation:", min_value=0)
    Verification_percent = st.sidebar.number_input("Verification Percent:", min_value=0.0, max_value=1.0, step=0.01)
    ID_Resolution_Match_percent = st.sidebar.number_input("ID Resolution Match Percent:", min_value=0.0, max_value=1.0, step=0.01)

    if st.sidebar.button("Predict"):
        if (Monthly_Traffic > 0 and Cost_Per_Acquisition > 0 and 0 <= Sales_Conversion_Rate <= 1.0
            and Deal_Value > 0 and 0 <= Re_opt_in_percent <= 1.0
            and 0 <= Re_activation_Sales_Rate <= 1.0
            and Cost_Per_Match_Reactivation >= 0 and 0 <= Verification_percent <= 1.0
            and 0 <= ID_Resolution_Match_percent <= 1.0):
            
            calculated_values = calculate_super_pixel_metrics(
                Monthly_Traffic, Cost_Per_Acquisition, Sales_Conversion_Rate, Deal_Value,
                Re_opt_in_percent, Re_activation_Sales_Rate, Cost_Per_Match_Reactivation,
                Verification_percent, ID_Resolution_Match_percent
            )
            
            st.sidebar.markdown("### Results")
            st.sidebar.markdown("---")
            
            for key, value in calculated_values.items():
                if key == "CPA(After)":
                    st.sidebar.metric(key, f"${value:.2f}")
                else:
                    st.sidebar.metric(key, f"${value:,}")

 
def display_calculated_values_as_table(calculated_values):
    st.markdown('## Metrics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue", f"${calculated_values['Revenue']:,}")
        st.metric("Sales", f"${calculated_values['Sales']:,}" if 'Sales' in calculated_values else "$0")
        st.metric("Estimated Spend", f"${calculated_values['Estimated Spend']:,}")

    with col2:
        st.metric("Recovered Revenue", f"${calculated_values['Recovered Revenue']:,}")
        st.metric("Recovered Sales", f"${calculated_values['Recovered Sales']:,}")
        st.metric("Recovered Leads", calculated_values['Recovered Leads'])
        st.metric("CPA(After)", f"${calculated_values['CPA(After)']:.2f}")

    with col3:
        st.metric("Anonymous Traffic", calculated_values['Anonymous Traffic'])
        st.metric("Verified Matched Profiles", calculated_values['Verified Matched_Profiles'])
        st.metric("Consumer Matches", calculated_values['Consumer Matches'])

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(r"C:\Users\DELL\Desktop\Codes\Sales PipeLine Forecast Model 2023 - SuperPixel.csv")


   
if __name__ == "__main__":
    if "csv_file_exists" not in st.session_state:
        st.session_state.csv_file_exists = False
    main()
