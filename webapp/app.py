import streamlit as st 
import time 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

def main():
    ref = db.reference("/")
    all = ref.get()
    power = all["power"]
    # data, power = all["data"], all["power"]
    # cur_time = list(data)[-1]
    # cur = data[cur_time]

    placeholder = st.empty()
    placeholder.text(f"Database State: {power}")

    if st.button("Toggle On or Off"): 
        print(f"{power=}")
        if power == "1": 
            ref.update({"power": "0"})
        elif power =="0": 
            ref.update({"power": "1"})
        new_power = ref.get()["power"]
        placeholder.text(f"Database State: {new_power}")

    # st.write(cur)

if __name__ == "__main__":
   
    if not firebase_admin._apps:
        #  # For LOCAL
        # cred = credentials.Certificate('cred.json')
        # default_app = firebase_admin.initialize_app(cred, {
        #     'databaseURL':"https://temp-humidity-sensor-747b7-default-rtdb.asia-southeast1.firebasedatabase.app" 
        # })

        # For PROD
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

