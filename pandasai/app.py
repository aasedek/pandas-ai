import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.data_loader.loader import DatasetLoader

st.set_page_config(page_title="PandasAI", page_icon="🐼")

st.title("🐼 PandasAI")

def main():
    """
    Main function to run the Streamlit application.
    """
    st.sidebar.title("Data Source")
    data_source = st.sidebar.radio("Select data source", ("Upload CSV/Parquet", "Connect to Database"))

    df = None

    if data_source == "Upload CSV/Parquet":
        uploaded_file = st.sidebar.file_uploader("Upload your file", type=["csv", "parquet"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".parquet"):
                    df = pd.read_parquet(uploaded_file)
            except Exception as e:
                st.error(f"Error reading file: {e}")

    elif data_source == "Connect to Database":
        st.sidebar.subheader("Database Connection")
        db_type = st.sidebar.selectbox("Database Type", ["mysql", "postgres"])
        host = st.sidebar.text_input("Host")
        port = st.sidebar.number_input("Port", value=3306 if db_type == "mysql" else 5432)
        database = st.sidebar.text_input("Database")
        user = st.sidebar.text_input("User")
        password = st.sidebar.text_input("Password", type="password")
        table = st.sidebar.text_input("Table")

        if st.sidebar.button("Connect"):
            try:
                # Create a connection string
                conn_str = f"{db_type}://{user}:{password}@{host}:{port}/{database}"

                # Load the data from the database
                loader = DatasetLoader()
                df = loader.load_sql(conn_str, table)
                st.success("Connected to the database and loaded the data!")
            except Exception as e:
                st.error(f"Error connecting to database: {e}")


    if df is not None:
        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Chat with your data")
        query = st.text_input("Ask a question about your data")

        if query:
            llm = OpenAI()
            sdf = SmartDataframe(df, config={"llm": llm})
            response = sdf.chat(query)
            st.write(response)

if __name__ == "__main__":
    main()
