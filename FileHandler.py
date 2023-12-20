from datetime import datetime
import xml.dom.minidom
import streamlit as st
import pandas as pd

from garmin_fit_sdk import Decoder, Stream, Profile



def import_file(file, filetype):
    # TODO change function to file format
    if filetype=='tcx':
        return import_tcx_file(file)
    elif filetype=='fit':
        return import_fit_file(file)
    else:
        return None

@st.cache_data
def import_tcx_file(file):
    tree = xml.dom.minidom.parse(file)
    root = tree.documentElement

    trackpoints = root.getElementsByTagName('Trackpoint')
    trackpoint_map = {}

    heartrate = 0
    speed = 0.0
    for trackpoint in trackpoints:
        time = trackpoint.getElementsByTagName('Time')[0].firstChild.nodeValue
        timestamp = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')

        heartrate_bpm = trackpoint.getElementsByTagName('HeartRateBpm')

        if heartrate_bpm.length > 0:
            heartrate = int(heartrate_bpm[0].getElementsByTagName('Value')[0].firstChild.nodeValue)

        distance = float(trackpoint.getElementsByTagName('DistanceMeters')[0].firstChild.nodeValue)

        tcx = trackpoint.getElementsByTagName('Extensions')[0].getElementsByTagName('ns3:TPX')
        if tcx.length > 0:
            speed_tag = tcx[0].getElementsByTagName('ns3:Speed')
            if speed_tag.length > 0:
                speed = float(speed_tag[0].firstChild.nodeValue)
        trackpoint_map[timestamp] = [heartrate, speed, distance]

    df = pd.DataFrame.from_dict(trackpoint_map, orient='index', columns=['Heartrate', 'Speed', 'Distance'])
    df.index.name = "Time"
    return df

@st.cache_data
def import_fit_file(file):
    stream = Stream.from_bytes_io(file)
    decoder = Decoder(stream)
    record_fields = set()

    def mesg_listener(mesg_num, message):
        if mesg_num == Profile['mesg_num']['RECORD']:
            for field in message:
                record_fields.add(field)

    messages, errors = decoder.read(apply_scale_and_offset = True,
            convert_datetimes_to_dates = True,
            convert_types_to_strings = True,
            enable_crc_check = True,
            expand_sub_fields = False,
            expand_components = True,
            merge_heart_rates = True,
            )

    if len(errors) > 0:
        print(f"Something went wrong decoding the file: {errors}")
        return

    #print(record_fields)
    df = pd.json_normalize(messages, record_path='record_mesgs')
    df.index = df['timestamp']
    df.set_index('timestamp')
    df.index.name = "Time"
    df.rename(columns={'enhanced_speed': 'Speed', 'distance': 'Distance', 'heart_rate':'Heartrate'}, inplace=True)
    df.drop(columns=["timestamp"])
    return df
