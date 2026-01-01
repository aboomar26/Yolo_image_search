import json
from pathlib import Path
from PIL import Image
import io
import base64


def ensure_processed_dir(raw_path):
    raw_path = Path(raw_path)
    processed_path = raw_path.parent.parent / "processed" / raw_path.name
    processed_path.mkdir(parents = True , exist_ok = True)
    return processed_path




def save_metadata(metadata,raw_path):
    processed_path = ensure_processed_dir(raw_path)

    output_path = processed_path / "metadata.json"
    with open(output_path , 'w') as f:
        json.dump(metadata , f)
    return output_path




def load_metadata(metadata_path):
    metadata_path = Path(metadata_path)
    if not metadata_path.exists():
        processed_path = metadata_path.parent.parent / "processed"/ metadata_path.name
        if processed_path.exists():
            metadata_path = metadata_path
        else:
            raise FileNotFoundError(f"Metadata not found at {str(metadata_path)}")
        
    with open(metadata_path,'r') as f:
        return json.load(f)
    



def get_unique_classes_count(metadata):
    unique_classes = set()
    count_options = {}

    for item in metadata:
        for cls in item['detection']:
            unique_classes.add(cls['class'])
            if cls['class'] not in count_options:
                count_options[cls['class']] = set()
            count_options[cls['class']].add(cls['count'])

    unique_classes = sorted(unique_classes)
    for cls in count_options:
        count_options[cls] = sorted(count_options[cls])
    
    return unique_classes , count_options



def image_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")