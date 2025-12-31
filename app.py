import streamlit as st
import sys
import os
from pathlib import Path
import time

def init_session_state():
    session_default = {
        "image_dir" : "path",
        'option' :"process new image"
    }

    for key,value in session_default.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

st.set_page_config(page_title = "YOLO11 search app" , layout = "wide")
st.title("Computer Cision Powered Search Aoolication")


option = st.radio("choose an option" ,("process new image" , "Load eisting metadata"),
         horizontal = True)


if option == "process new image":
    with st.expander("process new image", expanded = True):
        col1,col2 = st.columns(2)
        with col1:
            image_dir = st.text_input("image directory path" , placeholder = "path/to/image")
        with col2:
            model_path = st.text_input("model weights path" , value = "yolo11m.pt")
        
        if st.button("Start Inferance"):
            if image_dir:
                try:
                    with st.spinner("processing..."):
                        time.sleep(3)
                        st.success("the process is done")
                    pass
                except Exception as e:
                    st.error(f"Error during inference: {e}")
            else:
                st.warning("Please enter an image directory path")



else:
    with st.expander("Load Existing Metadata" , expanded = True):
        metadata_path = st.text_input("metadata file path" , placeholder = "path/to/metadata.json")
        
        if st.button("Load Metadata"):
            if metadata_path:
                try:
                    with st.spinner("processing..."):
                        time.sleep(3)
                        st.success("the process is done")
                    pass
                except Exception as e:
                    st.error(f"Error Loading metadata: {e}")
            else:
                st.warning("Please enter an metadata file path")


