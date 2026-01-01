import streamlit as st
import sys
import os
from pathlib import Path
import time
import json
from PIL import Image , ImageDraw ,  ImageFont
from src.inference import YOLOv11iference
from  src.utils import save_metadata , load_metadata , get_unique_classes_count,image_to_base64





def init_session_state():
    session_default = {
        "metadata" : None,
        "unique_classes" : [],
        "count_options" : {},
        "search_results" : [],
        "search_params" :{
                    "Search_mode" : "Any od selected classes (OR)",
                    "selected_classes" : [],
                    "thresholds" : {}
                        },

        "show_boxes" : True,
        "grid_colums" : 3,
        "highlight_matches" : True
        
    }

    for key,value in session_default.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

st.set_page_config(page_title = "YOLO11 search app" , layout = "wide")
st.title("Computer Vision Powered Search Application")




# Custom CSS for perfect grid layout
st.markdown(f"""
<style>
/* Main container adjustments */
.st-emotion-cache-1v0mbdj {{
    width: 100% !important;
    height: 100% !important;
}}

/* Column container - critical for grid layout */
.st-emotion-cache-1wrcr25 {{
    max-width: none !important;
    padding: 0 1rem !important;
}}

/* Individual column styling */
.st-emotion-cache-1n76uvr {{
    padding: 0.5rem !important;
}}

/* Image cards */
.image-card {{
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    margin-bottom: 20px;
    background: #f8f9fa;
}}

.image-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}}

.image-container {{
    position: relative;
    width: 100%;
    aspect-ratio: 4/3;
}}

.image-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.meta-overlay {{
    padding: 10px;
    background: rgba(0,0,0,0.85);
    color: white;
    font-size: 13px;
    line-height: 1.4;
}}
</style>
""", unsafe_allow_html=True)




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
 

# serach functionality

if st.session_state.metadata:
    st.header("🔎 Search Engine")
    with st.container():
        st.session_state.search_params["search_mode"] = st.radio("search mode",("Any od selected classes (OR)" , "All selected classes (And)") ,horizontal = True)
        st.session_state.search_params["selected_classes"] = st.multiselect("choose to search for" , (st.session_state.unique_classes),placeholder = "Choose options" )

        if st.session_state.search_params["selected_classes"]:
            st.subheader("Count Thresholds (optional)")
            col = st.columns(len(st.session_state.search_params["selected_classes"]))

            for i,cls in enumerate(st.session_state.search_params["selected_classes"]):
                with col[i]:
                    st.session_state.search_params["thresholds"][cls] = st.selectbox(f"Max count for {cls}" , options =["None"] + st.session_state.count_options[cls] )

        if st.button("Search Images" , type = "primary") and st.session_state.search_params["selected_classes"]:
            results = []
            search_params = st.session_state.search_params

            for item in st.session_state.metadata:
                matches = False
                class_matches = {}

                for cls in search_params["selected_classes"]:
                    class_detections = [d for d in item["detection"] if d["class"] == cls]
                    class_count = len(class_detections)

                    class_matches[cls] = False
                    threshold = search_params["thresholds"].get(cls, "None")

                    if threshold == "None":
                        class_matches[cls] = (class_count >= 1)

                    else :
                         class_matches[cls] = (class_count >= 1 and  class_count <= int(threshold))

                

                if search_params["search_mode"] == "Any od selected classes (OR)":
                    matches = any(class_matches.values())
                else:  # And mode
                    matches = all(class_matches.values())

                if matches:
                    results.append(item)

            st.session_state.search_results = results



if st.session_state.search_results:
    results = st.session_state.search_results
    search_params = st.session_state.search_params

    st.subheader(f"📷 Results: {len(results)} matching images")


    with st.expander("Display options" , expanded = True):
        cols = st.columns(3)
        with cols[0]:
            st.session_state.show_boxes = st.checkbox(
                "show bounding boxes" , 
                value = st.session_state.show_boxes)
            

        with cols[1]:
            st.session_state.grid_colums = st.slider(
                "Grid columns" 
                ,min_value = 2, max_value = 6, 
                value = st.session_state.grid_colums)
            

        with cols[2]:
            st.session_state.highlight_matches = st.checkbox(
                "Highlight matching classes" , 
                value = st.session_state.highlight_matches)

        
    
    grid_cols = st.columns(st.session_state.grid_colums)
    col_index = 0

    for result in results:
        with grid_cols[col_index]:

            try:
                img = Image.open(result['image_path'])
                draw = ImageDraw.Draw(img)

                if st.session_state.show_boxes:
                    try:
                            
                            font = ImageFont.truetype("arrial.ttf",12)
                    except:
                        font = ImageFont.load_default()

                    for det in result["detection"]:
                        cls = det["class"]
                        bbox = det["bbox"]

                        if cls in search_params["selected_classes"]:
                            color = "#FF4B4B"
                            thickness = 3

                        elif not st.session_state.highlight_matches:
                            color = "#666666"
                            thickness = 1
                        else:
                            continue
                    

                        draw.rectangle(bbox , outline = color ,width = thickness)

                        if cls in search_params['selected_classes'] or not st.session_state.highlight_matches:

                            label = f"{cls} {det['confidance']:.2f}"
                            text_bbox = draw.textbbox((0,0) , label ,font = font)
                            text_width = text_bbox[2] - text_bbox[0]
                            text_height = text_bbox[3] - text_bbox[1]

                            draw.rectangle([bbox[0] , bbox[1] , bbox[0] + text_width + 8 , bbox[1] + text_height + 4],
                                            fill = color)
                            
                            draw.text(
                                (bbox[0] + 4,bbox[1] + 2),
                                label,
                                fill = "white" ,
                                font = font
                            )

                meta_items = [f"{k} : {v}" for k , v in result['class_counts'].items()
                                if k in search_params["selected_classes"]]
                
                st.markdown(f"""
                <div class="image-card">
                    <div class="image-container">
                        <img src="data:image/png;base64,{image_to_base64(img)}">
                    </div>
                    <div class="meta-overlay">
                        <strong>{Path(result['image_path']).name}</strong><br>
                        {", ".join(meta_items) if meta_items else "No matches"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error displaying {result['image_path']} : {e}")
                
        col_index = (col_index + 1) % st.session_state.grid_colums

    with st.expander("Export Options"):
        st.download_button(
            label = "Download Results (JSON)" , 
            data = json.dumps(results , indent = 2),
            file_name = "search_results.json",
            mime = "application/json"
        )





