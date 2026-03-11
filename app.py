import streamlit as st
import pandas as pd
from agent import set_dataframe, data_cleaning_agent
from tools import plot_null_values, plot_distributions, plot_correlation_heatmap, plot_before_after

st.set_page_config(
    page_title="Data Cleaning & visualization Agent",
    page_icon="📊",
    layout="wide"
)

st.title("CSV Data Cleaning & Visualization Agent")

csv_file=st.file_uploader(
    "Upload csv dataset", type=['csv'], help="Upload a csv dataset for cleaning and visualization"
)

if csv_file:
    df=pd.read_csv(csv_file)
    original_df=df.copy()

    st.subheader("Raw Data Preview")
    st.dataframe(df)
    st.write(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    if st.button("Clean and Analyze Data"):
        set_dataframe(df)

        with st.spinner("Agent is analyzing and cleaning your data..."):
            try:
                response=data_cleaning_agent.run(
                    "Analyze and clean this dataset. Start with summary, check for issues, clean the data, and provide a final report."
                )

                st.subheader("Agent Analysis and Cleaning Report")
                st.markdown(response.content)

                col1, col2=st.columns(2)

                with col1:
                    st.plotly_chart(plot_null_values(original_df), use_container_width=True)
                    st.plotly_chart(plot_correlation_heatmap(df), use_container_width=True)
                with col2:
                    st.plotly_chart(plot_before_after(original_df, df), use_container_width=True)
                    st.plotly_chart(plot_distributions(df), use_container_width=True)
                
                st.header("Cleaned Data")
                st.dataframe(df)

                csv=df.to_csv(index=False)
                st.download_button(
                    label="Download Cleaned CSV",
                    data=csv,
                    file_name="cleaned_data.csv",
                    mime="text/csv"
                )

            except Exception as error:
                st.error(f"An error occured: {error}")
    
else:
    st.info("Please upload a CSV file to get started")