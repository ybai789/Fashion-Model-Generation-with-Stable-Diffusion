### Introduction

This project augments the Stable Diffusion WebUI by incorporating the Segment Anything Model (SAM) and ControlNet, specifically designed to generate garment model images. The application supports text prompts and offers both manual and automatic masking for image-to-image (img2img) generation, enhancing user control and flexibility. By leveraging pre-trained LoRA (Low-Rank Adaptation) models, it efficiently adapts to diverse cultural styles.

### Key Features

- **Stable Diffusion Integration**: Harnesses the Stable Diffusion API to produce high-quality images conditioned on user-provided text prompts, ensuring that the generated content aligns with the desired description.
- **Segment Anything Model (SAM)**: Utilizes SAM for precise segmentation, enabling accurate identification and extraction of garment regions within images, which is crucial for detailed analysis and manipulation.
- **ControlNet**: Employs ControlNet to adjust and control specific attributes of the generated images, ensuring consistency and alignment with desired garment characteristics.
- **Pre-trained LoRA Models**: Incorporates externally trained LoRA models to adapt the generation process to various cultural styles without the need for additional fine-tuning, streamlining the workflow.
- **Text Prompt Support**: Allows users to input descriptive text prompts, guiding the model toward generating images that match the provided description, thereby enhancing the relevance and accuracy of the outputs.
- **Manual and Automatic Masking**: Offers users the flexibility to manually select regions of interest or utilize automatic masking for img2img generation, providing greater control over the editing and generation process.

## Demo

<img src=".\images\demo.gif" alt="demo" />

 

## Usage

### 1. Install Stable Diffusion WebUI 

To begin, install the Stable Diffusion WebUI:

1. **Download**: Access the [Stable Diffusion WebUI Releases Page](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases) and download.

2. **Install**: Run the downloaded installer and follow the on-screen instructions to complete the installation.

### 2. Install Required Plugins 

Enhance the WebUI functionality by installing the following plugins:

1. **sd-webui-additional-networks**:

2. **sd-webui-controlnet**:

3. **sd-webui-segment-anything**:

### 3. Install Dependencies

```bash
pip install gradio
```

### 4. Download Stable Diffusion Model and LoRA Files

Obtain the necessary Stable Diffusion model and LoRA file from reputable sources (e.g. https://civitai.com/). Place these files in the designated directories.

### 5. Launch the Stable Diffusion Web UI 

- **Windows**:
  ```
  webui-user.bat
  ```

- **Unix/Linux**:
  ```
  ./webui.sh
  ```

Once initialized, access the WebUI interface through your browser.

### 6. Run the Main Script

Clone this repo and execute the main script to begin image generation:

```bash
python main.py
```

 