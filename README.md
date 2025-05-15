# PATRICIA OS
Command line interface built upon sensor technologies, tone generation, and music production techniques using Python and Ableton Live.

## Setup Guide

### Requirements

Python 3.13 (Make sure Python 3.13 is installed on your system. You can verify by running python3 --version in a terminal).

### Step 1: Download and Unzip the Project

First, download the project archive (e.g., a .zip file) from the source provided. Save it to a convenient location on your computer. Once the download is complete, unzip the archive to extract the project files. This will create a project folder containing all the necessary files.

### Step 2: Open a Terminal and Navigate to the Project Directory

Next, open your Terminal (on macOS/Linux) or Command Prompt/PowerShell (on Windows). Use the cd command to change into the project directory you just unzipped.

```cd ~/Downloads/patricia-os```

### Step 3: Create and Activate a Virtual Environment
It's recommended to use a Python virtual environment for this project to isolate its dependencies. Python 3.13 comes with the built-in venv module to create virtual environments.
1. Create the virtual environment: 
Run the following command in the project directory:
```python3.13 -m venv .venv```
2. Use one of the following commands based on your operating system:

#### macOS/Linux: ```source .venv/bin/activate```

#### Windows (Command Prompt): ```.venv\Scripts\activate.bat```

#### Windows (PowerShell): ```.\venv\Scripts\Activate.ps1```

After activation, your command prompt should change to include (.venv), indicating the virtual environment is active. All Python commands will now use this isolated Python 3.13 environment.

### Step 4: Install Dependencies from requirements.txt

With the virtual environment activated, install the project’s required Python packages. The project should include a file named requirements.txt that lists all the dependencies. Use pip to install these by running:

```pip install -r requirements.txt```

If you see a warning about pip being out of date, you can upgrade it by running: 

```python -m pip install --upgrade pip```

### Step 5: Run the Application

You’re now ready to run the project’s main program. Ensure you are still in the project directory and that your virtual environment is activated (you should see the (.venv) in your terminal prompt). Then execute the main Python file:

```python main.py```

This will launch the application. If everything is set up correctly, the program should start running using Python 3.13 and the installed dependencies. (If your system prompts for camera access or if you encounter a webcam error on first run, see the Note below.)

### Note

The first time you run the program, you may encounter an error like:

```RuntimeError: [Face Detector] Error opening webcam.```

This error occurs because the Terminal (command line) application does not yet have permission to use your computer’s camera. To fix this on macOS, go to System Settings and navigate to Privacy & Security > Camera, then find and enable camera access for your Terminal application. After granting the Terminal permission to access the camera, run python main.py again. The program should now be able to open the webcam without error.