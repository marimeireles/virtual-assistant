# How to use this project

1. Create a virtual environment using your fav tool
2. Using a Python >= 3 `pip install PySide2`
3. `git clone https://github.com/RasaHQ/rasa-demo.git
cd rasa-demo`
4. `pip install -e .`
5. rasa train --augmentation 0
6. `pip3 install deepspeech`
7. `wget https://github.com/mozilla/DeepSpeech/releases/download/v0.5.1/deepspeech-0.5.1-models.tar.gz
tar xvfz deepspeech-0.5.1-models.tar.gz`
8. Run `python main.py`

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

# Resources that might be useful to me

## NLP

* https://rasa.com/docs/rasa/nlu/about/
* https://github.com/RasaHQ/rasa-demo
* https://vimeo.com/254777331

## The channels problem

* https://rasa.com/docs/rasa/api/agent/
* https://stackoverflow.com/questions/51019885/using-rasa-nlu-model-with-python-api-instead-of-http-server
* https://forum.rasa.com/t/need-some-help-posting-to-socket-io-server/1422
* https://forum.rasa.com/t/how-to-create-custom-channel-instead-of-socketio-channel/13711
* https://github.com/RasaHQ/rasa/tree/master/rasa/core/channels

## Interesting more or less related stuff

* http://www.peterbloem.nl/blog/transformers

## Cute stuff

* Threads: https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/
