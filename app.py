import streamlit as st
import sys
import os
from pathlib import Path
import time
from src.inference import YOLOv11iference
from  src.utils import save_metadata , load_metadata , get_unique_classes_count


def init_session_state():
    session_default = {
        "metadaat" : None,
        "unique_classes" : [],
        "count_options" : {},
    }

    for key,value in session_default.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

st.set_page_config(page_title = "YOLO11 search app" , layout = "wide")
st.title("Computer Cision Powered Search Application")


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
                        inference = YOLOv11iference(model_path)
                        metadata = inference.process_directory(image_dir)
                        metadata_path = save_metadata(metadata,image_dir)
                        st.success(f"processed {len(metadata)} images. metadata sves to:")
                        st.code(str(metadata_path))
                        st.session_state.metadata = metadata
                        st.session_state.unique_classes , st.session_state.count_options=get_unique_classes_count(metadata)
                    
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
                        metadata = load_metadata(metadata_path)
                        st.session_state.metadata = metadata
                        st.session_state.unique_classes , st.session_state.count_options=get_unique_classes_count(metadata)
                        st.success(f"successfully loaded metadata for  {len(metadata)} images.")
                    pass
                except Exception as e:
                    st.error(f"Error Loading metadata: {e}")
            else:
                st.warning("Please enter an metadata file path")
 

