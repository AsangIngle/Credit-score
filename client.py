import streamlit as st
from app import process_json

st.set_page_config(page_title="Aave V2 Credit Score", layout="wide")
st.title(" Aave V2 Wallet Credit Scoring")

uploaded_file = st.file_uploader("Upload `user-wallet-transactions.json`", type="json")

if uploaded_file is not None:
    st.info("Processing file...")
    output_df, error = process_json(uploaded_file)

    if error:
        st.error(error)
    else:
        st.success("Wallet credit scores generated successfully!")
        st.dataframe(output_df)

        csv = output_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="wallet_credit_scores.csv",
            mime="text/csv"
        )
