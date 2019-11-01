import QtQuick.Window 2.2
import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtGraphicalEffects 1.13
// import QtWebKit 3.0

//main layout
ApplicationWindow {
    id: window
    title: qsTr("Voice Assistant")
    width: 1280
    height: 960
    visible: true
    Label {
        id: pageTitle
        text: ""
        font.pixelSize: 20
        anchors.centerIn: parent
    }

//widgets layout
    Page {
        width: 639
        height: 960
        anchors.left: parent.left
        id: widget
        Image {
            id: sine
            anchors.top: parent.top
            anchors.margins: 12
            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            source: "sine.png"
            visible: false
        }

        ShaderEffect {
            id: shader
            anchors.fill: sine
            property variant source: sine
            property real frequency: 4
            property real amplitude: 0.3
            property real time: 0.5 
            NumberAnimation on time {
                id: shadertime
                from: 0; to: Math.PI*2; duration: 10000; loops: Animation.Infinite
            }
            fragmentShader: "
                            varying highp vec2 qt_TexCoord0;
                            uniform sampler2D source;
                            uniform lowp float qt_Opacity;
                            uniform highp float frequency;
                            uniform highp float amplitude;
                            uniform highp float time;
                            void main() {
                                highp vec2 texCoord = qt_TexCoord0;
                                texCoord.y = amplitude * sin(time * frequency + texCoord.x * 6.283185) + texCoord.y;
                                gl_FragColor = texture2D(source, texCoord) * qt_Opacity;
                            }"
        }

//just a dirty trick in case I don't finish until Monday. You just have to click in this
//smily face to stop the wave from waveing. click only once though :)
        Image {
            id: qt_bot
            anchors.bottom: parent.bottom
            anchors.margins: 350
            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            source: "qt_bot_face.png"

            MouseArea {
                anchors.fill: parent
                onClicked:
                {
                    shadertime.pause();
                }
            }
        }

        Image {
            id: mic
            anchors.bottom: parent.bottom
            anchors.margins: 12
            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            source: "mic.png"

            MouseArea {
                anchors.fill: parent
                onClicked:
                {
                    audio_recorder.toggle_record();
                    if (shadertime.paused) {
                        shadertime.resume();
                    }
                    else {
                        shadertime.pause();
                    }
                }
            }
        }

    //separator
        Page {
            width: 2
            height: 960
            anchors.right: parent.right
            Rectangle {
                width: 2
                height: 100
                border.color: "white"
                border.width: 5
            }
            Rectangle {
                width: 2
                height: 860
                border.color: "lightgrey"
                border.width: 5
            }
            Rectangle {
                width: 2
                height: 100
                border.color: "white"
                border.width: 5
            }
        }
    }

//chat layout
    Page {
        width: 639
        height: 960
        anchors.right: parent.right
        id: chat

        ColumnLayout {
            anchors.fill: parent

            ListView {
                id: listView
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.margins: pane.leftPadding + messageField.leftPadding
                displayMarginBeginning: 40
                displayMarginEnd: 40
                verticalLayoutDirection: ListView.BottomToTop
                spacing: 12
                model: chat_model
                delegate: Column {
                    readonly property bool sentByMe: model.recipient !== "Me"
                    anchors.right: sentByMe ? parent.right : undefined
                    spacing: 6

                    Row {
                        id: messageRow
                        spacing: 6
                        anchors.right: sentByMe ? parent.right : undefined

                        Rectangle {
                            width: Math.min(messageText.implicitWidth + 24, listView.width - messageRow.spacing)
                            height: messageText.implicitHeight + 24
                            radius: 15
                            color: sentByMe ? "lightgrey" : "#ff627c"

                            Label {
                                id: messageText
                                text: model.message
                                color: sentByMe ? "black" : "white"
                                anchors.fill: parent
                                anchors.margins: 12
                                wrapMode: Label.Wrap
                            }
                        }
                    }

                    Label {
                        id: timestampText
                        text: Qt.formatDateTime(model.timestamp, "d MMM hh:mm")
                        color: "lightgrey"
                        anchors.right: sentByMe ? parent.right : undefined
                    }
                }

                ScrollBar.vertical: ScrollBar {}
            }

            Pane {
                id: pane
                Layout.fillWidth: true

                RowLayout {
                    width: parent.width

                    TextArea {
                        id: messageField
                        Layout.fillWidth: true
                        placeholderText: qsTr("Compose message")
                        wrapMode: TextArea.Wrap
                    }

                    Button {
                        id: sendButton
                        text: qsTr("Send")
                        enabled: messageField.length > 0
                        onClicked: {
                            audio_recorder.on_transcription_finished(messageField.text);
                            messageField.text = "";
                        }
                    }
                }
            }
        }
    }
}
