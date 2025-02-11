import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("GDP Analysis Dashboard")
st.write("Upload a CSV file containing GDP data.")

# File Uploader
uploaded_file = st.file_uploader("Upload GDP CSV File", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Ensure required columns exist
    required_columns = {'Country Name', 'Year', 'Value'}
    if not required_columns.issubset(df.columns):
        st.error(f"CSV must contain columns: {required_columns}")
    else:
        df["Year"] = df["Year"].astype(int)  # Ensure Year is an integer

        final = []

        # Process GDP Growth Calculation
        for country in df['Country Name'].unique():
            df_all = df[df['Country Name'] == country].copy()
            df_all = df_all.sort_values(by="Year")  # Ensure correct order

            gdp_growth = [0]  # First year has no growth rate

            for i in range(1, len(df_all)):
                curr = df_all.iloc[i]["Value"]
                prev = df_all.iloc[i - 1]["Value"]

                # Handle zero-division case
                if prev == 0:
                    gdp_growth.append(0)
                else:
                    gdp_growth.append(round((curr - prev) / prev * 100, 2))

            df_all["GDP Growth (%)"] = gdp_growth
            final.append(df_all)

        df = pd.concat(final, axis=0)

        # Display Top 10 Countries by Maximum GDP Value
        top_gdp_countries = df.groupby('Country Name')['Value'].max().sort_values(ascending=False).head(10)

        st.subheader("Top 10 Countries by Maximum GDP Value")
        st.dataframe(top_gdp_countries)

        # Plot GDP Trends
        st.subheader("GDP Growth Trend for a Selected Country")
        country = st.selectbox("Select a Country", df["Country Name"].unique())

        if country:
            df_country = df[df["Country Name"] == country]

            # Plot
            fig, ax = plt.subplots()
            ax.plot(df_country["Year"], df_country["GDP Growth (%)"], marker='o', linestyle='-')
            ax.set_xlabel("Year")
            ax.set_ylabel("GDP Growth (%)")
            ax.set_title(f"GDP Growth Trend of {country}")
            ax.grid(True)
            st.pyplot(fig)
