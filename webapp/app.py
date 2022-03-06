import streamlit as st 
import time 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import pandas as pd 
from datetime import datetime

def main():
    ref = db.reference("/")
    all = ref.get()
    data, power = all["data"], all["power"]
    cur_time = list(data)[-1]
    cur = data[cur_time]
    print(cur)
    temperature = cur["Temperature"]
    humidity = cur["Humidity"]

    cur_datetime = datetime.fromtimestamp(int(cur_time))
    st.text(cur_datetime)
    

    power_snapshot = st.empty()
    data_snapshot = st.empty()
    col1, col2, col3 = st.empty(), st.empty(), st.empty()
    col1, col2, col3 = st.columns(3)
    # col1.metric(label="Power", value=power)
    # col2.metric(label="Temperature", value = f"{temperature} °C" )
    # col3.metric(label="Humidity", value = f"{humidity} % ")

    if st.button("Toggle On or Off"): 
        print(f"{power=}")
        if power == "1": 
            ref.update({"power": "0"})
        elif power =="0": 
            ref.update({"power": "1"})
        new_power = ref.get()["power"]
        col1.metric(f"Database State: {new_power}")

    if st.button("Update"):
        new_power =ref.get()["power"]
        new_data = ref.get()["data"] 
        new_cur = new_data[list(new_data)[-1]]
        col1.metric(label="Power", value=new_power)
        new_temperature = new_cur["Temperature"]
        new_humidity = new_cur["Humidity"]
        col2.metric(label="Temperature", value = f"{new_temperature} °C" )
        col3.metric(label="Humidity", value = f"{new_humidity} % ")

    if st.button("Process Data"):
        df = pd.DataFrame.from_dict(data, orient='index')
        # df.index.name = "Time"
        df = df.reset_index()
        print(df.keys())
        df["index"] = df["index"].apply(lambda x: datetime.fromtimestamp(int(x)))
        df = df.set_index('index')
        st.dataframe(data=df)
        st.line_chart(data=df["Humidity"])
        st.line_chart(data=df["Temperature"])

if __name__ == "__main__":
   
    if not firebase_admin._apps:
        #  # For LOCAL
        # cred = credentials.Certificate('cred.json')
        # default_app = firebase_admin.initialize_app(cred, {
        #     'databaseURL':"https://temp-humidity-sensor-747b7-default-rtdb.asia-southeast1.firebasedatabase.app" 
        # })

        For PROD
        default_app = firebase_admin.initialize_app(
            credentials.Certificate({
                "type": "service_account",
                "project_id": os.environ["project_id"],
                "private_key": os.environ["private_key"],
                "private_key": os.environ.get('private_key').replace('\\n', '\n'),
                "client_email": os.environ["client_email"],
                "token_uri": "https://oauth2.googleapis.com/token",
            }), 
            {
                'databaseURL':"https://temp-humidity-sensor-747b7-default-rtdb.asia-southeast1.firebasedatabase.app" 
            })
    

    main()

