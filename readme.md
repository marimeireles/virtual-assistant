# How to use this project

1. Create a virtual environment using your fav tool
2. Using a Python >= 3.5 `pip install PySide2 && pip install rasa && pip install deepspeech` or use the requirements file
3. `wget https://github.com/mozilla/DeepSpeech/releases/download/v0.5.1/deepspeech-0.5.1-models.tar.gz
tar xvfz deepspeech-0.5.1-models.tar.gz`
4. `git clone https://github.com/mozilla/TTS.git && cd TTS && git checkout db7f3d3`
5. `python setup.py develop`
6. Download from [here](https://drive.google.com/drive/folders/1GU8WGix98WrR3ayjoiirmmbLUZzwg4n0) these two files: "config.json" and "best_model.th.tar"
7. Create a directory inside your main directory called `tts_model` and put the recently downloaded stuff there
8. `cd qt-rasa && rasa train`
9. On `qt-rasa` directory run `rasa run --enable-api -p 5002 -vv`
10. On the main directory run `python main.py` to open the GUI

# License

Please note that this code is under Qt License.

Copyright (C) 2019 The Qt Company Ltd.
Contact: http://www.qt.io/licensing/

This file is part of the provisioning scripts of the Qt Toolkit.

$QT_BEGIN_LICENSE:LGPL21$
Commercial License Usage
Licensees holding valid commercial Qt licenses may use this file in
accordance with the commercial license agreement provided with the
Software or, alternatively, in accordance with the terms contained in
a written agreement between you and The Qt Company. For licensing terms
and conditions see http://www.qt.io/terms-conditions. For further
information use the contact form at http://www.qt.io/contact-us.

GNU Lesser General Public License Usage
Alternatively, this file may be used under the terms of the GNU Lesser
General Public License version 2.1 or version 3 as published by the Free
Software Foundation and appearing in the file LICENSE.LGPLv21 and
LICENSE.LGPLv3 included in the packaging of this file. Please review the
following information to ensure the GNU Lesser General Public License
requirements will be met: https://www.gnu.org/licenses/lgpl.html and
http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.

As a special exception, The Qt Company gives you certain additional
rights. These rights are described in The Qt Company LGPL Exception
version 1.1, included in the file LGPL_EXCEPTION.txt in this package.