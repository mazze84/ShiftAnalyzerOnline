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









