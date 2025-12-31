from ultralytics import YOLO
from pathlib import Path
# import torch
# from PIL import Image
# import numpy
from src.config import load_config

class YOLOv11iference:
    def __init__(self,model_name,device='cuda'):
        
        self.device = device
        self.model = YOLO(model_name)
        self.model.to(self.device)
        
        
        #loading config from default.yaml
        config = load_config()
        self.conf_threshold = config["model"]["conf_threshold"]
        self.image_extensions = config["data"]["image_extensions"]


    def process_image(self,image_path):

        results = self.model.predict(
            source = image_path,
            conf = self.conf_threshold,
            device =self.device
        )

        detection = []
        class_counts = {}

        for result in results:
            for box in result.boxes:
                cls = result.names[int(box.cls)]
                conf = float(box.conf)
                bbox = box.xyxy[0].tolist()

                detection.append({
                    'class' : cls,
                    'confidance' : conf,
                    'bbox' : bbox,
                    'count' : 1
                })

                class_counts[cls] = class_counts.get(cls,0) + 1

        for det in detection:
            det['count'] = class_counts[det['class']]

        return {
            'image_path' : str(image_path),
            'detection': detection,
            'total_objects' : len(detection),
            'unique_class' : list(class_counts.keys()),
            'class_counts' : class_counts
        }

    def process_directory(self , directory):
        metadata = []

        paterns = [f"*{ext}"  for ext in self.image_extensions]

        image_paths = []

        for patern in paterns :
            image_paths.extend(Path(directory).glob(patern))


        for img_path in image_paths:
            try:
                metadata.append(self.process_image(img_path)) 
            except Exception as e:
                print(f"Error processing {img_path} : {str(e)}")

        return metadata


        