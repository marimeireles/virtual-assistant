# Project aestethics

![aesthetics](https://psychonautgirl.space/images/project_aesthetics.png)

# How to use:

## Unix users:

### Setup

1. Create a virtual environment using your favorite tool
2. Using a Python >= 3.5 `pip install PySide2 rasa deepspeech torch` or use the requirements file
3. Download the model from DeepSpeech's repo and unzip it `wget https://github.com/mozilla/DeepSpeech/releases/download/v0.5.1/deepspeech-0.5.1-models.tar.gz tar xvfz deepspeech-0.5.1-models.tar.gz`
4. To download and checkout to the correct branch of our TTS tool `git clone https://github.com/mozilla/TTS.git && cd TTS && git checkout db7f3d3`
5. `python setup.py develop` . This step may take a while because Mozilla TTS will install everything it needs to train a model, also, depending on your python version you might need to compile the dependencies.
6. Download from [here](https://drive.google.com/drive/folders/1GU8WGix98WrR3ayjoiirmmbLUZzwg4n0) these two files: "config.json" and "best_model.th.tar". They are the configuration that we're going to use for TTS and the best model available at the time this tutorial was first created. TTS is constantly improving and you can access new, better models [here](https://github.com/mozilla/TTS/wiki/Released-Models)
7. If you're still in the TTS directory we just created `cd ..` to the main directory. Create a directory inside of it called `tts_model` and put the files downloaded in step 6 there
8. `cd qt-rasa && rasa train`\*

### Running your assistant

9. On `qt-rasa` directory run `rasa run --enable-api -p 5002 -vv` to start the NLP server
10. On the main directory run `python main.py` to open the GUI

## Window users:

### Setup

1. Create a virtual environment using your favorite tool
2. Using a Python >= 3.5 `pip install PySide2 rasa deepspeech torch` or use the requirements file
3. [Download](http://gnuwin32.sourceforge.net/packages/wget.htm) wget if you don't have it. To test it simply type `wget --version` in your terminal
4. Download the model from DeepSpeech's repo `wget https://github.com/mozilla/DeepSpeech/releases/download/v0.5.1/deepspeech-0.5.1-models.tar.gz`
5. If you have MinGW/MSYS or Cygwin installed, you can use the tar command to unpack the file `tar xvfz deepspeech-0.5.1-models.tar.gz`. If you prefer to use a GUI tool to unzip it try [7zip](https://www.7-zip.org/)
6. To download and checkout to the correct branch of our TTS tool `git clone https://github.com/mozilla/TTS.git && cd TTS && git checkout db7f3d3`
7. `python setup.py develop` . This step may take a while because Mozilla TTS will install everything it needs to train a model, also, depending on your python version you might need to compile the dependencies.
8. Download from [here](https://drive.google.com/drive/folders/1GU8WGix98WrR3ayjoiirmmbLUZzwg4n0) these two files: "config.json" and "best_model.th.tar". They are the configuration that we're going to use for TTS and the best model available at the time this tutorial was first created. TTS is constantly improving and you can access new, better models [here](https://github.com/mozilla/TTS/wiki/Released-Models)
9. If you're still in the TTS directory we just created `cd ..` to the main directory. Create a directory inside of it called `tts_model` and put the files downloaded in step 8 there
11. `cd qt-rasa && rasa train`\*

### Running your assistant

12. On `qt-rasa` directory run `rasa run --enable-api -p 5002 -vv`
13. On the main directory run `python main.py` to open the GUI

\* Every time you change something in the .md files you'll have to retrain this
