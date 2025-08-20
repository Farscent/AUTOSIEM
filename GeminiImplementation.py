
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import google.generativeai as genai

# Gemini API Configuration:
try:
    GEMINI_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
except (FileNotFoundError, KeyError):
    st.error("Google API Key not found. Please set it in your Streamlit secrets.")
    st.stop()

# Load Data and Model:
@st.cache_data # Use st.cache_data to load data only once
def load_data():
    # Data.zip is a zipped CSV file, so use compression='zip'
    df = pd.read_csv("Data.zip", compression='zip')
    # Limit to 20% of the data for performance
    df = df.sample(frac=0.2, random_state=42).reset_index(drop=True)
    model_local = joblib.load("xgboost_fraud_model.joblib")

    # Select the same features used for training
    features = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
    X = df[features]

    # Generate predictions and add them to the DataFrame
    predictions = model_local.predict(X)
    df['predictedFraud'] = predictions
    df['hour'] = df['step'] % 24

    return df, model_local

df, model_local = load_data()
df_fraud = df[df['predictedFraud'] == 1].copy() # Create a separate df for fraudulent transactions
# Add is_drained column: True if newbalanceOrig == 0, else False
df_fraud['is_drained'] = df_fraud['newbalanceOrig'] == 0

# Initial Page Configuration:
st.set_page_config(
    page_title="Gemini-Powered SIEM Dashboard",
    layout="wide",
)

# Sidebar (after df and model are loaded):
with st.sidebar:
    st.header("Natural Language Query")
    user_query = st.text_input("Ask a question about the data:")

    if user_query:
        with st.spinner("Generating query..."):
            schema = pd.io.json.build_table_schema(df)
            prompt = f"""
            Given this pandas DataFrame schema, convert the user's question into a valid pandas query.
            Only return the code. Schema: {schema}. Question: {user_query}.
            DataFrame is named 'df'.
            """
            response = model.generate_content(prompt)
            code_to_run = response.text.replace("`", "").replace("python", "")

            st.code(code_to_run)
            try:
                result_df = eval(code_to_run)
                st.dataframe(result_df)
            except Exception as e:
                st.error(f"Could not execute query: {e}")

# Dashboard Title:
st.title("SIEM Dashboard for Fraud Detection")
st.markdown("This dashboard provides an overview and summary of the transactions")

# KPI Section:
st.header("Key Performance Indicators")

total_transactions = len(df)
total_fraudulent = len(df_fraud)
fraud_rate = (total_fraudulent / total_transactions) * 100 if total_transactions > 0 else 0
total_fraud_amount = df_fraud['amount'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Fraudulent Transactions", f"{total_fraudulent:,}")
col3.metric("Fraud Rate", f"{fraud_rate:.4f}%")
col4.metric("Total Fraud Amount", f"${total_fraud_amount:,.2f}")

# Visualization Section:
st.header("Transaction Analysis")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["Fraud Overview", "Amount Analysis", "Top Offenders"])

with tab1:
    st.subheader("General Fraud Landscape")
    
    col1, col2 = st.columns([2, 1]) # Give more space to the sunburst chart
    
    with col1:
        # Pie chart for a clearer breakdown
        st.write("**Fraud Breakdown: Account Drained vs Partial Amount**")
        pie_data = df_fraud.copy()
        pie_data['Drain Status'] = pie_data['is_drained'].apply(lambda x: 'Account Drained' if x else 'Partial Amount')
        drain_counts = pie_data['Drain Status'].value_counts().reset_index()
        drain_counts.columns = ['Drain Status', 'Count']
        fig_pie = px.pie(drain_counts, names='Drain Status', values='Count',
                        title="Proportion of Fraudulent Transactions by Drain Status",
                        color='Drain Status',
                        color_discrete_map={
                            'Account Drained': '#1f77b4',
                            'Partial Amount': '#ff7f0e'
                        })
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Key metrics derived from the data
        st.write("**Key Insights**")
        most_common_hour = df_fraud['hour'].mode()[0]
        avg_fraud_amount = df_fraud['amount'].mean()
        
        st.metric("Most Common Fraud Hour", f"{most_common_hour}:00")
        st.metric("Avg. Fraudulent Amount", f"${avg_fraud_amount:,.2f}")
        st.info("Insight: Fraud is concentrated in **TRANSFER** and **CASH_OUT** types, often resulting in the full depletion of the source account.")

    # Bar chart for activity by hour
    st.subheader("Fraudulent Activity by Hour of Day")
    fraud_by_hour = df_fraud.groupby('hour').size().reset_index(name='count')
    fig_hour = px.bar(fraud_by_hour, x='hour', y='count', 
                      labels={'hour': 'Hour of Day (in 24h format)', 'count': 'Number of Fraudulent Transactions'})
    st.plotly_chart(fig_hour, use_container_width=True)


with tab2:
    st.subheader("Analysis of Transaction Amounts")
    
    # Violin plot for clearer distribution visualization
    st.write("**How are transaction amounts distributed for fraud vs. legitimate?**")
    st.markdown("A violin plot shows the full distribution and density of transaction amounts for each class. This helps you see not just the median, but also how amounts are spread and where outliers occur.")
    fig_violin = px.violin(
        df,
        x='predictedFraud',
        y='amount',
        color='predictedFraud',
        box=True,
        points='all',
        title='Transaction Amount Distribution by Fraud Status',
        labels={'predictedFraud': 'Fraudulent (1) vs Legitimate (0)', 'amount': 'Transaction Amount'},
        color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
    )
    st.plotly_chart(fig_violin, use_container_width=True)
    st.info("**Insight:** The violin plot shows both the spread and density of transaction amounts. Fraudulent transactions (1) tend to have higher and more variable amounts compared to legitimate (0). Outliers are also easier to spot.")

    # Scatter plot to spot outliers over time
    st.write("**Fraudulent Transaction Amounts Over Time**")
    fig_scatter = px.scatter(df_fraud, x='step', y='amount', 
                             title="Fraudulent Amounts vs. Time Step",
                             labels={'step': 'Time Step', 'amount': 'Transaction Amount'},
                             hover_data=['nameOrig', 'nameDest'])
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.info("**Insight:** Use this chart to identify specific high-value fraudulent transactions and when they occurred. Hover over points for account details.")


with tab3:
    st.subheader("Identifying Top Fraudulent Actors")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Top 10 Origin Accounts by Fraud Amount**")
        top_10_origin = df_fraud.groupby('nameOrig')['amount'].sum().nlargest(10).reset_index()
        st.dataframe(top_10_origin)

    with col2:
        st.write("**Top 10 Destination Accounts by Fraud Amount**")
        top_10_dest = df_fraud.groupby('nameDest')['amount'].sum().nlargest(10).reset_index()
        st.dataframe(top_10_dest)
        
    st.info("**Insight:** These tables pinpoint the primary accounts involved in the largest fraudulent activities, providing clear targets for investigation.")



# Gemini Helper Functions:

def get_smart_alert(transaction_data):
    prompt = f"""
    Analyze this transaction flagged as fraudulent and provide a concise alert summary for a SOC analyst.
    Highlight suspicious elements like full balance transfers.
    Data: {transaction_data.to_json()}
    """
    response = model.generate_content(prompt)
    return response.text


def get_investigation_timeline(account_id):
    history = df[(df['nameOrig'] == account_id) | (df['nameDest'] == account_id)].sort_values('step').tail(10)
    prompt = f"""
    Given the recent transaction history for an account involved in a fraudulent alert, 
    construct a likely attack timeline in bullet points.
    History: {history.to_json(orient='records')}
    """
    response = model.generate_content(prompt)
    return response.text


# Alert Triage Section:
st.header("Live Fraud Alerts")
st.dataframe(df_fraud[['step', 'type', 'amount', 'nameOrig', 'nameDest', 'oldbalanceOrg', 'newbalanceOrig']].head(10))

# Smart Alert & Investigation Section:
st.header("Smart Investigation Workbench")
selected_index = st.selectbox("Select a Fraudulent Transaction to Investigate:", df_fraud.index)

if selected_index:
    selected_transaction = df_fraud.loc[selected_index]
    origin_account = selected_transaction['nameOrig']

    st.subheader("Gemini-Powered Smart Alert")
    with st.spinner('Generating smart alert...'):
        smart_alert = get_smart_alert(selected_transaction)
        st.info(smart_alert)

    st.subheader(f"Automated Investigation Timeline for Account: {origin_account}")
    with st.spinner(f'Building timeline for {origin_account}...'):
        timeline = get_investigation_timeline(origin_account)
        st.markdown(timeline)


# Pop Down Section for All Fraudulent Originators:
st.header("Detailed Fraud Investigation")
with st.expander("Show All Fraudulent Originators and Amounts Stolen"):
    fraud_by_origin = df_fraud.groupby('nameOrig')['amount'].sum().sort_values(ascending=False).reset_index()
    fraud_by_origin.columns = ['Origin Account', 'Total Stolen Amount']
    st.dataframe(fraud_by_origin)


