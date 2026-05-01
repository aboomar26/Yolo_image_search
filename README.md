# YOLO11 Image Search Application

A powerful computer vision-powered image search application that leverages YOLO11 (YOLOv11) object detection to enable intelligent image searching based on detected objects. Built with Streamlit for an intuitive and responsive web interface.

## 🎯 Overview

This application enables you to:
- **Batch Process Images**: Process entire directories of images automatically using YOLO11
- **Intelligent Search**: Find images based on detected object classes with flexible search modes
- **Advanced Filtering**: Filter results by object count thresholds and confidence scores
- **Visual Analysis**: View detections with bounding boxes, confidence scores, and color-coded highlights
- **Persistent Metadata**: Save and load detection metadata for faster subsequent searches
- **Export Capabilities**: Download search results and metadata as JSON

## ✨ Key Features

- **Dual Search Modes**:
  - **OR Mode**: Find images containing ANY of the selected object classes
  - **AND Mode**: Find images containing ALL of the selected object classes
- **Flexible Filtering**: Set maximum count thresholds for specific object types
- **Rich Visualization**:
  - Bounding boxes around detected objects
  - Confidence scores for each detection
  - Color-coded highlighting for matched classes
  - Customizable grid layout (2-6 columns)
- **Metadata Management**:
  - Save detection results to avoid reprocessing
  - Load previously saved metadata for faster searches
  - Export results as JSON for external analysis
- **GPU Acceleration**: Optional CUDA support for significantly faster processing

## 📋 System Requirements

- **Python**: 3.11 or higher
- **GPU** (optional): CUDA-capable GPU recommended for faster processing
- **Storage**: Sufficient disk space for model weights (~50MB) and image processing
- **RAM**: Minimum 4GB (8GB+ recommended for batch processing)

## 🚀 Installation

### Prerequisites
- Conda (Anaconda or Miniconda)
- Git (optional, for version control)

### Option 1: CPU Installation

```bash
conda create -n yolo_image_search python=3.11 -y
conda activate yolo_image_search
pip install -r requirements.txt
```

### Option 2: GPU Installation (Recommended for faster processing)

```bash
conda create -n yolo_image_search_gpu python=3.11 -y
conda activate yolo_image_search_gpu
conda install pytorch==2.5.1 torchvision==0.20.1 pytorch-cuda=12.4 -c pytorch -c nvidia
pip install -r requirements.txt
```

### GPU Setup Notes

For GPU acceleration, ensure CUDA is properly installed:

**Linux Users:**
- [CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)

**Windows Users:**
- [CUDA Installation Guide for Windows](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/)

**Verification:**
```bash
nvidia-smi  # Check if CUDA is available
```

**Troubleshooting:**
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/whats-the-relationship-between-cuda-toolkit-and-pytorch/251096/2)

## 📦 Project Structure

```
Yolo_image_search/
├── app.py                      # Main Streamlit web application
├── yolo11m.pt                  # Pre-trained YOLO11 Medium model weights
├── requirements.txt            # Python package dependencies
├── instruction.txt             # Setup instructions
├── README.md                   # Project documentation (this file)
├── configs/
│   └── default.yaml           # Configuration file for model and data settings
└── src/
    ├── inference.py           # YOLO11 inference engine class
    ├── config.py              # Configuration loader utilities
    └── utils.py               # Helper functions for metadata and image processing
```

## ⚙️ Configuration

The application uses `configs/default.yaml` for configuration. Customize as needed:

```yaml
model:
  yolo_model: "yolo11m.pt"         # Model weights file path
  conf_threshold: 0.3              # Confidence threshold (0.0-1.0) for object detection

data:
  image_extensions: ['.jpg', '.jpeg', '.png']  # Supported image file formats
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `yolo_model` | string | `yolo11m.pt` | Path to YOLO model weights |
| `conf_threshold` | float | `0.3` | Minimum confidence for detections (0-1) |
| `image_extensions` | list | `['.jpg', '.jpeg', '.png']` | Supported image formats |

## 🎮 Usage Guide

### Starting the Application

```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`

### Workflow

#### Step 1: Load Detection Data

Choose one of two options:

**Option A: Process New Images**
1. Select "Process new images" from the sidebar
2. Enter the directory path containing your images
3. Specify the YOLO model weights path (default: `yolo11m.pt`)
4. Click "Start Inference"
5. Wait for processing to complete (time varies based on image count and hardware)

**Option B: Load Existing Metadata**
1. Select "Load metadata" from the sidebar
2. Choose previously saved metadata file
3. Metadata and detection results will be loaded instantly

#### Step 2: Configure Search Parameters

1. **Select Search Mode**:
   - **OR Mode**: Returns images with ANY selected class
   - **AND Mode**: Returns images with ALL selected classes

2. **Choose Object Classes**:
   - Select from available detected classes
   - Multiple selections allowed

3. **Set Count Thresholds** (optional):
   - Limit results based on object counts
   - Useful for finding images with specific quantities

#### Step 3: View and Export Results

1. **Visualization Options**:
   - Toggle bounding boxes on/off
   - Toggle class highlighting
   - Adjust grid layout (2-6 columns)

2. **Export Results**:
   - Download search results as JSON
   - Use for further analysis or integration

## 📚 Dependencies

See `requirements.txt` for complete list:

- **ultralytics**: YOLO11 implementation
- **streamlit**: Web application framework
- **opencv-python**: Image processing
- **torch**: Deep learning framework
- **torchvision**: Computer vision utilities
- **pillow**: Image manipulation
- **pyyaml**: Configuration file handling
- **pandas**: Data manipulation
- **numpy**: Numerical computing

## 🔧 Troubleshooting

### Application Won't Start
```bash
# Verify Streamlit installation
streamlit --version

# Clear Streamlit cache
streamlit cache clear

# Run with verbose output
streamlit run app.py --logger.level=debug
```

### CUDA/GPU Issues
```bash
# Verify GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvidia-smi
```

### Out of Memory Errors
- Process fewer images per batch
- Reduce image resolution in preprocessing
- Use CPU mode for testing

### Slow Processing
- Ensure GPU drivers are up to date
- Check if GPU is being utilized: `nvidia-smi -l 1`
- Consider using a lighter model (yolo11s.pt instead of yolo11m.pt)

## 📝 License

[Add your license information here]

## 👤 Author

Created as part of the CV Udemy course projects.

## 🤝 Support

For issues, questions, or contributions, please refer to the project repository.

---

**Last Updated**: May 2026
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


