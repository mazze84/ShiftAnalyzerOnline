import streamlit as st
from io import StringIO
import pandas as pd
import FileHandler as fh
import ShiftAnalyzer as sa

st.set_page_config(
    page_title="Shift Analyzer",
    page_icon="🏒",
)

def draw_page(df):
    df_shifts = sa.calc_shift_len(df)

    st.line_chart(data=df, x="time_diff", y=["Heartrate", "HFMinMax"], color=["#00F08F", "#FF0000"])
    st.line_chart(data=df, x="time_diff", y=["Speed_rolling", "SpeedMinMax"], color=["#00F08F", "#0000FF"])

    st.bar_chart(data=df_shifts, y="Duration", color='Active')
    option = st.selectbox('Show only active shifts?', ('All', 'Shift', 'Bench'))
    st.write('You selected:', option)
    if "Shift" == option:
        df_active = df_shifts[df_shifts["Active"] == True]
        duration_mean = round(df_active["Duration"].mean(),2)
        st.metric(label="avg. Duration", value=duration_mean)
        hr_mean = round(df_active["Average Heartrate"].mean())
        st.metric(label="avg. Heartrate", value=hr_mean)
        speed_mean = round(df_active["Average Speed"].mean(),2)
        st.metric(label="Average Speed", value=speed_mean)

        st.table(df_active[["Duration", "Average Heartrate", "Average Speed"]])
    elif "Bench" == option:
        df_bench = df_shifts[df_shifts["Active"] == False]
        duration_mean = round(df_bench["Duration"].mean(),2)
        st.metric(label="avg. Duration", value=duration_mean)
        st.table(df_bench[["Duration", "Average Heartrate", "Average Speed"]])
    else:
        st.table(df_shifts[["Duration", "Average Heartrate", "Average Speed"]])



st.title('Shift Analyzer')
st.write("# ")
st.markdown(
    """
    Welcome to Hockey Shift Analyzer! 🏒 
    Drop a tcx or fit file to analyze your hockey shifts from speed data
    
    If you have feedback please go to the GitHub repository 
    
    ### Want to learn more?
    Check out [GitHub repo](https://github.com/mazze84/ShiftAnalyzerOnline)
"""
)

uploaded_file = st.file_uploader("Upload a .fit or .tcx file for shift analysis", type=['tcx','fit'])
if uploaded_file is not None:
    df = None
    if uploaded_file.name[-3:] == 'tcx':
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        df = fh.import_file(stringio, uploaded_file.name[-3:])
        df = sa.interpret_data(df)
        draw_page(df)
    elif uploaded_file.name[-3:] == 'fit':
        df = fh.import_fit_file(uploaded_file)
        df = sa.interpret_data(df)
        draw_page(df)









