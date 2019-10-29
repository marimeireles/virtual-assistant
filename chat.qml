import QtQuick.Window 2.2
import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12

import SqlConversationModel 1.0
// import AudioRecorder 1.0

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
            anchors.bottom: parent.bottom
            anchors.margins: 12
            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            source: "mic.png"

            //fazer uma imagenzinha bonitinha e onclicked mudar a imagem pra ter umas ondinha saindo dela?

            //no topo eu ainda posso colocar as sine wave
            MouseArea {
                anchors.fill: parent
                onClicked: { audioRecorder.toggleRecord() }
                }
            }

    //     Button {
    //         anchors.bottom: parent.bottom
    //         anchors.margins: 12
    //         id: myButton
    //         objectName: "myButton"
    //         x: (parent.width - width) / 2
    //         y: (parent.height - height) / 2
    //         text: "Record"
    //         onClicked: {}

    // }

        //2 POSSIBILITY
        // Rectangle {
        //     width: 100; height: 100
        //     color: "red"

        //     SequentialAnimation on x {
        //         loops: Animation.Infinite
        //         PropertyAnimation { to: 50 }
        //         PropertyAnimation { to: 0 }
        //     }
        // }

        //1 POSSIBILITY
        // ShaderEffect {
        //     anchors.fill: parent
        //     property variant source: sourceImg
        //     property real frequency: 1
        //     property real amplitude: 0.1
        //     property real time: 0.0
        //     NumberAnimation on time {
        //         from: 0; to: Math.PI*2; duration: 10000; loops: Animation.Infinite
        //     }
        // Image {
        //     id: sourceImg
        //     anchors.fill: parent
        //     source: "learning_qml/chapter5-styling/Albert_Einstein.png"
        //     visible: false
        // }
        //     fragmentShader: "
        //                     varying highp vec2 qt_TexCoord0;
        //                     uniform sampler2D source;
        //                     uniform lowp float qt_Opacity;
        //                     uniform highp float frequency;
        //                     uniform highp float amplitude;
        //                     uniform highp float time;
        //                     void main() {
        //                         highp vec2 texCoord = qt_TexCoord0;
        //                         texCoord.y = amplitude * sin(time * frequency + texCoord.x * 6.283185) + texCoord.y;
        //                         gl_FragColor = texture2D(source, texCoord) * qt_Opacity;
        //                     }"
        // }

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
                model: SqlConversationModel {}
                delegate: Column {
                    anchors.right: sentByMe ? parent.right : undefined
                    spacing: 6

                    readonly property bool sentByMe: model.recipient !== "Me"

                    Row {
                        id: messageRow
                        spacing: 6
                        anchors.right: sentByMe ? parent.right : undefined

                        Rectangle {
                            width: Math.min(messageText.implicitWidth + 24, listView.width - messageRow.spacing)
                            height: messageText.implicitHeight + 24
                            radius: 15
                            color: sentByMe ? "lightgrey" : "steelblue"

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
                            listView.model.sendMessage("machine", messageField.text);
                            messageField.text = "";
                        }
                    }
                }
            }
        }
    }
}
