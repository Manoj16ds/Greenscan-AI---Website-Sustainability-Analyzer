import streamlit as st
import main  # your existing backend file

st.set_page_config(page_title="GreenScan AI")

st.title(" GreenScan AI - Eco Website Analyzer")

st.write("Analyze your website’s sustainability by measuring page size, image load, and estimated carbon footprint.")

# Input field for website URL
url = st.text_input("Enter Website URL (e.g. https://example.com):")

if st.button("Analyze Website"):
    if not url.strip():
        st.warning("Please enter a valid website URL.")
    else:
        with st.spinner("Scanning website and analyzing sustainability..."):
            try:
                result = main.run_greenscan(url)
                st.success(" Analysis Completed!")
                st.write(result)

                # If report or charts are generated
                st.download_button(" Download Report (PDF)", open("greenscan_report.pdf", "rb"), file_name="greenscan_report.pdf")

                st.image("classification_pie.png", caption="Image Classification", use_column_width=True)
                st.image("carbon_vs_size.png", caption="Carbon vs Page Size", use_column_width=True)
                st.image("emission_comparison.png", caption="Emission Comparison", use_column_width=True)
            except Exception as e:
                st.error(f"Error during analysis: {e}")
