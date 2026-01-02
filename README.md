# YOLO11 Image Search Application

A powerful computer vision-powered image search application that uses YOLO11 (YOLOv11) object detection to enable semantic image searching based on detected objects. Built with Streamlit for an intuitive web interface.

## 🎯 Overview

This application allows you to:
- Process entire directories of images using YOLO11 object detection
- Search images based on detected object classes
- Filter results by object count thresholds
- Visualize detections with bounding boxes and confidence scores
- Save and load metadata for faster subsequent searches

## ✨ Features

- **Batch Image Processing**: Process entire directories of images automatically
- **Advanced Search Modes**:
  - **OR Mode**: Find images containing ANY of the selected classes
  - **AND Mode**: Find images containing ALL of the selected classes
- **Count Thresholds**: Filter results by maximum count of specific objects
- **Visualization**:
  - Display bounding boxes on detected objects
  - Highlight matching classes with different colors
  - Customizable grid layout (2-6 columns)
- **Metadata Management**: Save and load detection metadata for faster searches
- **Export Results**: Download search results as JSON

## 📋 Requirements

- Python 3.11+
- CUDA-capable GPU (optional, but recommended for faster processing)
- PyTorch (CPU or GPU version)

## 🚀 Installation

### Option 1: CPU Installation

```bash
conda create -n yolo_image_search python=3.11 -y
conda activate yolo_image_search
pip install -r requirements.txt
```

### Option 2: GPU Installation (Recommended)

```bash
conda create -n yolo_image_search_gpu python=3.11 -y
conda activate yolo_image_search_gpu
conda install pytorch==2.5.1 torchvision==0.20.1 pytorch-cuda=12.4 -c pytorch -c nvidia
pip install -r requirements.txt
```

**Note**: For GPU installation, ensure you have CUDA installed. See the [CUDA Installation Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) for Linux or [Windows CUDA Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/) for Windows.

## 📦 Project Structure

```
Yolo_image_search/
├── app.py                 # Main Streamlit application
├── yolo11m.pt            # YOLO11 model weights
├── requirements.txt      # Python dependencies
├── configs/
│   └── default.yaml      # Configuration file
├── src/
│   ├── inference.py      # YOLO11 inference class
│   ├── config.py         # Configuration loader
│   └── utils.py          # Utility functions
└── README.md             # This file
```

## ⚙️ Configuration

Edit `configs/default.yaml` to customize:

```yaml
model:
  yolo_model: "yolo11m.pt"
  conf_threshold: 0.3  # Confidence threshold for detections

data:
  image_extensions: ['.jpg', '.jpeg', '.png']  # Supported image formats
```

## 🎮 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Step 1: Process Images or Load Metadata

**Option A: Process New Images**
1. Select "Process new image" option
2. Enter the path to your image directory
3. Specify the model weights path (default: `yolo11m.pt`)
4. Click "Start Inference"
5. Wait for processing to complete
6. Metadata will be automatically saved

**Option B: Load Existing Metadata**
1. Select "Load existing metadata"
2. Enter the path to your previously saved `metadata.json` file
3. Click "Load Metadata"

### Step 2: Search Images

1. **Choose Search Mode**:
   - **Any of selected classes (OR)**: Returns images containing at least one of the selected classes
   - **All selected classes (AND)**: Returns images containing all selected classes

2. **Select Classes**: Choose one or more object classes to search for from the dropdown

3. **Set Count Thresholds** (Optional):
   - For each selected class, optionally set a maximum count threshold
   - Leave as "None" to match any count

4. **Click "Search Images"** to see results

### Step 3: View and Export Results

- **Display Options**:
  - Toggle bounding boxes on/off
  - Adjust grid columns (2-6)
  - Highlight matching classes

- **Export**: Download search results as JSON using the export button

## 📊 Metadata Format

The application generates metadata in the following JSON format:

```json
{
  "image_path": "path/to/image.jpg",
  "detection": [
    {
      "class": "person",
      "confidance": 0.95,
      "bbox": [x1, y1, x2, y2],
      "count": 2
    }
  ],
  "total_objects": 2,
  "unique_class": ["person"],
  "class_counts": {
    "person": 2
  }
}
```

## 🔧 Technical Details

- **Model**: YOLO11 (YOLOv11) Medium variant (`yolo11m.pt`)
- **Framework**: Ultralytics YOLO
- **UI Framework**: Streamlit
- **Image Processing**: PIL (Pillow)
- **Configuration**: YAML-based configuration system

## 📝 Notes

- The application automatically saves metadata to a `processed/` directory relative to your image directory
- Supported image formats: `.jpg`, `.jpeg`, `.png` (configurable in `default.yaml`)
- For best performance, use GPU acceleration when processing large image directories
- The model weights file (`yolo11m.pt`) should be in the project root directory

## 🐛 Troubleshooting

- **CUDA errors**: Ensure PyTorch is installed with CUDA support matching your GPU's CUDA version
- **Model not found**: Verify that `yolo11m.pt` exists in the project root or provide the correct path
- **Image processing errors**: Check that image paths are correct and images are in supported formats

## 📚 Resources

- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [CUDA Installation Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)


