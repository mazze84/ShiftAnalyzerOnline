import streamlit as st
from io import StringIO
import pandas as pd
import FileHandler as fh
import ShiftAnalyzer as sa

st.set_page_config(
    layout='wide',
    page_title="Shift Analyzer",
    page_icon="🏒",
)

def draw_page(df):
    df, df_shifts = sa.calc_shift_len(df)
    st.line_chart(data=df, x="time_diff", y=["Heartrate", "HFMinMax"], color=["#00F08F", "#FF0000"])
    st.line_chart(data=df, x="time_diff", y=["Speed_rolling", "SpeedMinMax"], color=["#00F08F", "#0000FF"])

    multiselect = st.multiselect("Show only select shifts", df_shifts.index.to_series(), df_shifts.index.to_series())
    st.bar_chart(data=df_shifts.filter(items=multiselect, axis=0), y="Duration", color='Active')
    option = st.selectbox('Show only shifts?', ('All', 'Shift', 'Bench'))

    df_filtered = df_shifts.filter(items=multiselect, axis=0)
    df_active = df_filtered[df_filtered["Active"] == True]
    df_bench = df_filtered[df_filtered["Active"] == False]
    if "Shift" == option:
        col1,col2,col3 = st.columns([1,1,1])
        duration_mean = round(df_active["Duration"].mean(),2)
        with col1:
            st.metric(label="avg. Duration", value=duration_mean)
        hr_mean = round(df_active["Average Heartrate"].mean())
        with col2:
            st.metric(label="avg. Heartrate", value=hr_mean)
        speed_mean = round(df_active["Average Speed"].mean(),2)
        with col3:
            st.metric(label="Average Speed", value=speed_mean)
        st.table(df_active[["Duration", "Average Heartrate", "Average Speed"]])
    elif "Bench" == option:
        duration_mean = round(df_bench["Duration"].mean(),2)
        st.metric(label="avg. Duration", value=duration_mean)
        st.table(df_bench[["Duration", "Average Heartrate", "Average Speed"]])
    else:
        col1, col2, col3 = st.columns([1, 1, 1])
        duration_shift_mean = round(df_active["Duration"].mean(),2)
        duration_bench_mean = round(df_bench["Duration"].mean(),2)
        with col1:
            st.metric(label="avg. duration shift", value=duration_shift_mean)
            st.metric(label="avg. duration bench", value=duration_bench_mean)
        hr_shift_mean = round(df_active["Average Heartrate"].mean())
        hr_bench_mean = round(df_bench["Average Heartrate"].mean())
        with col2:
            st.metric(label="avg. HR shift", value=hr_shift_mean)
            st.metric(label="avg. HR bench", value=hr_bench_mean)
        speed_shift_mean = round(df_active["Average Speed"].mean(), 2)
        speed_bench_mean = round(df_bench["Average Speed"].mean(), 2)
        with col3:
            st.metric(label="avg. speed shift", value=speed_shift_mean)
            st.metric(label="avg. speed bench", value=speed_bench_mean)
        st.table(df_filtered[["Duration", "Average Heartrate", "Average Speed"]])


st.title('Shift Analyzer')
st.write("# ")
st.markdown(
    """
    Welcome to Hockey Shift Analyzer! 🏒 
    Drop a tcx or fit file to analyze your hockey shifts from speed data
    
    If you have feedback please go to the GitHub repository 
    
    ### Want to learn more?
    Check out the [GitHub repo](https://github.com/mazze84/ShiftAnalyzerOnline)
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









