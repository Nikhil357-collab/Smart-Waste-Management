import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from fetch_data import get_thingspeak_data

# Auto refresh every 15 seconds
st_autorefresh(
    interval=15000,
    key="refresh"
)

st.set_page_config(
    page_title="Smart Waste Management",
    page_icon="♻",
    layout="wide"
)

st.title("♻ Smart Waste Management Dashboard")

try:

    df = get_thingspeak_data()

    if df.empty:
        st.warning("No data available.")
        st.stop()

except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

latest = df.iloc[-1]

distance = float(latest["field1"])
fill = float(latest["field2"])
status_code = int(float(latest["field3"]))
alert_code = int(float(latest["field4"]))

    
df["field1"] = pd.to_numeric(df["field1"], errors="coerce")
df["field2"] = pd.to_numeric(df["field2"], errors="coerce")
df["field3"] = pd.to_numeric(df["field3"], errors="coerce")
df["field4"] = pd.to_numeric(df["field4"], errors="coerce")

df = df.dropna()

print(type(distance))
print(type(fill))
print(type(status_code))
print(type(alert_code))


status_map = {
    1: "EMPTY",
    2: "HALF FULL",
    3: "NEARLY FULL",
    4: "FULL"
}

status = status_map.get(
    int(status_code),
    "UNKNOWN"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Distance (cm)",
    f"{distance:.2f}"
)

col2.metric(
    "Fill Percentage",
    f"{fill:.2f}%"
)

col3.metric(
    "Status",
    status
)

col4.metric(
    "Alert",
    "ON" if alert_code == 1 else "OFF"
)

# Alert Box

if fill > 90:
    st.error("🚨 BIN FULL")
elif fill > 70:
    st.warning("⚠ BIN NEARLY FULL")
else:
    st.success("✅ BIN NORMAL")

# Analytics

avg_fill = df["field2"].mean()
max_fill = df["field2"].max()

col5, col6 = st.columns(2)

col5.metric(
    "Average Fill",
    f"{avg_fill:.2f}%"
)

col6.metric(
    "Maximum Fill",
    f"{max_fill:.2f}%"
)

# Prediction

df["field2"] = df["field2"].ffill()

if len(df) > 1:

    growth_rate = (
        df["field2"].iloc[-1]
        -
        df["field2"].iloc[0]
    ) / len(df)

    if growth_rate > 0:

        remaining = 100 - fill

        estimated_cycles = (
            remaining / growth_rate
        )

        estimated_minutes = (
            estimated_cycles * 15
        )

        st.info(
            f"Estimated Time To Full: "
            f"{estimated_minutes:.0f} minutes"
        )

# Fill Trend

fig1 = px.line(
    df,
    x="created_at",
    y="field2",
    title="Fill Percentage Trend"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Distance Trend

fig2 = px.line(
    df,
    x="created_at",
    y="field1",
    title="Distance Trend"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("Recent Data")

st.dataframe(
    df.tail(20),
    use_container_width=True
)