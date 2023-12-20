import streamlit as st
from io import StringIO
import pandas as pd
import FileHandler as fh
import ShiftAnalyzer as sa

def draw_page(df):

    df_shifts = sa.calc_shift_len(df)

    st.line_chart(data=df, x="time_index_seconds", y=["Heartrate", "HFMinMax"], color=["#00F08F", "#FF0000"])
    st.line_chart(data=df, x="time_index_seconds", y=["Speed_rolling", "SpeedMinMax"], color=["#00F08F", "#0000FF"])

    st.bar_chart(data=df_shifts, y="Duration", color='Active')
    option = st.selectbox('Show only active shifts?', ('All', 'Shift', 'Bench'))
    st.write('You selected:', option)
    if "Shift" == option:
        df_active = df_shifts[df_shifts["Active"] == True]
        duration_mean_df = df_active["Duration"].mean()
        st.write(duration_mean_df)
        st.table(df_active[["Duration", "Average Heartrate", "Average Speed"]])
    elif "Bench" == option:
        df_bench = df_shifts[df_shifts["Active"] == False]
        duration_mean_df = df_bench["Duration"].mean()
        st.write(duration_mean_df)
        st.table(df_bench[["Duration", "Average Heartrate", "Average Speed"]])
    else:
        st.table(df_shifts[["Duration", "Average Heartrate", "Average Speed"]])


st.header('Shift Analyzer')
uploaded_file = st.file_uploader("Upload a .fit or .tcx file for shift analysis", type=['tcx','fit'])
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    trackpoints = fh.import_tcx_file(stringio)
    df = sa.interpret_data(trackpoints)
    draw_page(df)







