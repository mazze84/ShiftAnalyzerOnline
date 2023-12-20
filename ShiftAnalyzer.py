import pandas as pd
import streamlit as st
@st.cache_data
def interpret_data(df):
    df['Speed_rolling'] = moving_average(df["Speed"], 5)
    df["time_index_seconds"] = time_index(df.index.to_series())
    df = time_index(df)
    return df

def time_index(df):
    calc_duration_seconds(df.index.min(), df.index.max())

    start_time = df.index.min()
    df['time_diff'] = df.index.to_series() - start_time
    return df

def shift(df_shifts):
    shifts = []
    for shift in df_shifts.to_dict('index').values():
        shifts.append("Shift" if shift['is_active'] else "Bench")
    df_shifts['Shift Desc']
    return df_shifts


def calc_shift_len(df, active_speed=0.2, seconds_inactive=10):
    shifts = []
    avg_heartrate = 0
    heartrate_cnt = 0
    avg_speed = 0

    trackpoints = df.to_dict('index')

    start_time = list(trackpoints.keys())[0]
    last_time = list(trackpoints.keys())[0]
    changed_time =  list(trackpoints.keys())[0]

    is_active = False#list(trackpoints.values())[0]['Speed_rolling'] > active_speed
    minMax= []
    minMaxHF = []
    print("----------------------------------------------------------")
    for time, trackpoint_list in trackpoints.items():
        speed = trackpoint_list['Speed_rolling']
        heartrate = trackpoint_list['Heartrate']

        changed = (is_active and speed <= active_speed) or (not is_active and speed > active_speed)
        if (not changed):
            changed_time = time
        if (is_active):
            minMax.append(6)
            minMaxHF.append(180)
        else:
            minMax.append(0)
            minMaxHF.append(0)

        if changed and calc_duration_seconds(changed_time, time) > seconds_inactive:
            # save shift
            duration_last_shift = calc_duration_seconds(start_time, last_time)
            shifts.append([start_time, time, calc_avg(avg_heartrate, heartrate_cnt),
                           calc_avg(avg_speed, heartrate_cnt, decimals=2), duration_last_shift, is_active])

            # reset values
            start_time = time
            avg_heartrate = heartrate
            avg_speed = speed
            heartrate_cnt = 1
            is_active = speed > active_speed
        else:
            avg_heartrate += heartrate
            heartrate_cnt += 1
            avg_speed += speed
            last_time = time



    df['SpeedMinMax'] = minMax
    df['HFMinMax'] = minMaxHF
    shifts.append([start_time, time, calc_avg(avg_heartrate, heartrate_cnt), calc_avg(avg_speed, heartrate_cnt, decimals=2), calc_duration_seconds(start_time, list(trackpoints.keys())[len(trackpoints)-1]), is_active])
    df_shifts = pd.DataFrame(shifts, columns=['Starttime', 'Endtime', 'Average Heartrate', 'Average Speed', 'Duration', 'Active'])
    df_shifts['Time_Diff'] = df_shifts['Starttime'] - df_shifts['Endtime']
    return df_shifts



# extracts column in matrix to list
def extract(lst, index):
    return [item[index] for item in lst]

def calc_duration_seconds(start_time, end_time):
    duration = end_time - start_time
    return duration.total_seconds()

def calc_avg(list, cnt, decimals=0):
    avg = 0
    if cnt > 0:
        list /= cnt
        avg = round(list, decimals)
    return avg

def moving_average(lst, rolling_cnt):
    numbers_series = pd.Series(lst)
    return numbers_series.rolling(rolling_cnt, min_periods=1).mean().tolist()