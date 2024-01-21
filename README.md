# KFM Tools
## Introduction
Kubic FLOTAC Microscope system requires data collection and analysis in order to obtain better results.
For this reason, KFM Tools have been developed. These are the functionalities provided by this toolkit:
- Images Labeler: Label the images in a folder and save labels with YOLOv8 format
- Camera Viewer: Concat images from scan session in order to have the chamber image
- Samples Scanner: Load the session zip file on AI server to start the prediction
- Results Analyzer: Get evaluation metrics by comparing results obtained with AI model with observations

## Setup
### Windows
- Open the Terminal by searching “cmd” in the search bar
- Write “python” to open the store where to get Python
- Install Python
- Go back to the Terminal and write “pip install numpy”
- Write “pip install Pillow”
- Write “pip install paramiko”
- Open the file kfm_tools.bat to launch the script without using the Terminal

### MacOS
- Open the Terminal
- Write "python3" to start the installation process of Command Line Developer Tools
- Install the Command Line Developer Tools
- Write "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py" on Terminal and launch
- Write "rm get-pip.py" on Terminal and launch
- Go back to the Terminal and write “pip3 install numpy”
- Write “pip3 install Pillow”
- Write “pip3 install paramiko”
- Write on Terminal "python3 " and drag the file kfm_tools.py to launch the script
