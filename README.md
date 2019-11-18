# Project aestethics

![aesthetics](https://psychonautgirl.space/images/interface.png)

# How to use:

1. Create a virtual environment using your fav tool
2. Using a Python >= 3.5 `pip install PySide2 && pip install rasa && pip install deepspeech` or use the requirements file
3. `wget https://github.com/mozilla/DeepSpeech/releases/download/v0.5.1/deepspeech-0.5.1-models.tar.gz
tar xvfz deepspeech-0.5.1-models.tar.gz`
4. `git clone https://github.com/mozilla/TTS.git && cd TTS && git checkout db7f3d3`
5. `python setup.py develop`
6. Download from [here](https://drive.google.com/drive/folders/1GU8WGix98WrR3ayjoiirmmbLUZzwg4n0) these two files: "config.json" and "best_model.th.tar"
7. Create a directory inside your main directory called `tts_model` and put the recently downloaded stuff there
8. `cd qt-rasa && rasa train`\*
9. On `qt-rasa` directory run `rasa run --enable-api -p 5002 -vv`
10. On the main directory run `python main.py` to open the GUI

\* Every time you change something in the .md files you'll have to retrain this

