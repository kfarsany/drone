import os
import gc
import kivy 
kivy.require('1.11.1')

from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import BooleanProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.progressbar import ProgressBar

import time
import threading
from PIL import Image
import cv2
import test
import ImageProcessing
import concurrent.futures
import SpeechRecognition as Speech

Window.fullscreen = 'auto'
Builder.load_string("""
<DroneView>:
    FloatLayout:
        id:simpleview
        Button:
            id: btnExit3
            text: "Exit"
            size_hint: 0.05, 0.05
            pos_hint: {'top': .99, 'right': .99}
            on_press: Factory.ExitPopup1().open() if not app.check_connect() else Factory.ExitPopup2().open()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Button:
            id: btnLeft
            text: "Left"
            on_press: None if app.left() else Factory.InvalidPopup1().open()
            size_hint: 0.15, 0.15
            pos_hint: {'top': 0.5, 'right': 0.2}
        Button:
            id: btnRight
            text: "Right"
            on_press: None if app.right() else Factory.InvalidPopup1().open()
            size_hint: 0.15, 0.15
            pos_hint: {'top': 0.5, 'right': 0.5}
        Button:
            id: btnBackward
            text: "Backward"
            on_press: None if app.backward() else Factory.InvalidPopup1().open()
            size_hint: 0.15, 0.15
            pos_hint: {'top': 0.5, 'right': 0.35}
        Button:
            id: btnForward
            text: "Forward"
            on_press: None if app.forward() else Factory.InvalidPopup1().open()
            size_hint: 0.15, 0.15
            pos_hint: {'top': 0.652, 'right': 0.35}
        Button:
            id: btnUp
            text: "Up"
            on_press: None if app.up() else Factory.InvalidPopup1().open()
            size_hint: 0.15, 0.15
            pos_hint: {'top': 0.652, 'right': 0.85}
        Button:
            id: btnDown
            text: "Down"
            on_press: None if app.down() else Factory.InvalidPopup1().open()
            size_hint: 0.15, 0.15
            pos_hint: {'top': 0.5, 'right': 0.85}
        Button:
            id: btnHover
            text: "Hover"
            on_press: None if app.hover() else Factory.InvalidPopup1().open()
            size_hint: 0.2, 0.2
            pos_hint: {'top': 0.9, 'right': 0.61}
            font_size: '20pt'
        Button:
            id: btnAbort3
            text: "ABORT!!!"
            size_hint: 0.3, 0.2
            pos_hint: {'top': 0.3, 'right': .66}
            on_press: app.abort()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
            font_size: '50pt'
        
<DroneAdvView>:
    FloatLayout:
        id: droneview
        Button:
            id: btnAbort1
            text: "ABORT!!!"
            size_hint: 0.05, 0.05
            pos_hint: {'top': .93, 'right': .99}
            on_press: app.abort()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Button:
            id: btnExit2
            text: "Exit"
            size_hint: 0.05, 0.05
            pos_hint: {'top': .99, 'right': .99}
            on_press: Factory.ExitPopup1().open() if not app.check_connect() else Factory.ExitPopup2().open()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Image:
            id: mapImage
            source: "Gmap/drone_path.png"
            size_hint: 0.4, 0.4
            pos_hint: {'right': .48, 'top': .99}
        Image:
            id: prescoreImage
            source: "images/prescored.png"
            size_hint: 0.25, 0.25
            pos_hint: {'right': .69, 'top': .4}
        Image:
            id: scoreImage
            source: "images/scored.png"
            size_hint: 0.25, 0.25
            pos_hint: {'right': .97, 'top': .4}
        Image:
            id: myexport
            size_hint: 0.4, 0.4
            pos_hint: {'right': .9, 'top': .88}
        Button:
            text: "Test Path"
            size_hint: 0.125, 0.1
            pos_hint: {'top': .4, 'right': 0.8}
            on_release: app.test_path()
        Label:
            id: score_label
            text: 'Score: '
            font_name: 'fonts/Gilberto.ttf'
            font_size: root.height*0.08
            pos_hint: {'top': 0.95, 'right': 1.2}
        Button:
            id: setTargets
            text: "Set Targets"
            size_hint: 0.125, 0.1
            pos_hint: {'top': .24, 'right': 0.27}
            on_press: app.find_start()
            on_release: setTargets.text = "Start"
            on_release: setTargets.disabled = False if setTargets.text == "Start" else None
            on_press: Factory.NumTargetsPopup().open() if not setTargets.text == "Start" else app.threading_read()
        Image:
            source: "images/target.png"
            size_hint: 0.2, 0.2
            pos_hint: {'top': .29, 'right': 0.46}
    FloatLayout:
        opacity: 1
        id: video
        VideoPlayer:
            opacity: 0
            id: audio
            state: 'play'
            volume: 0
        Button:
            id: H_Vol
            text: "Sound On"
            size_hint: 0.125, 0.07
            pos_hint: {'top': .95, 'right': 0.69}
            on_release: audio.volume = 1
        Button:
            id: L_Vol
            text: "Sound Off"
            size_hint: 0.125, 0.07
            pos_hint: {'top': .95, 'right': 0.84}
            on_release: audio.volume = 0

<ControllerView>:
#:import Factory kivy.factory.Factory
#:import time time

    FloatLayout:
        Button:
            id: btnExit1
            text: "Exit"
            size_hint: 0.05, 0.05
            pos_hint: {'top': .99, 'right': .99}
            on_press: Factory.ExitPopup1().open() if root.Setup else Factory.ExitPopup2().open()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        

    FloatLayout:
        opacity: 1 if root.Setup else 0
        Spinner:
            id: port_spinner
            size_hint: .06, .08
            pos_hint: {'top': .62, 'right': .36}
            text: 'None'
            values: app.available_ports()
            disabled: True if not root.Setup else False
        Spinner:
            id: baud_spinner
            size_hint: .06, .08
            pos_hint: {'top': .62, 'right': .76}
            text: 'None'
            values: '4800', '9600', '19200', '38400', '57600', '115200'
            disabled: True if not root.Setup else False
        Button:
            text: "Check"
            size_hint: 0.1, 0.08
            on_release: Factory.Check1Popup().open() if port_spinner.text == 'None' or baud_spinner.text == 'None' else Factory.Check2Popup().open()
            pos_hint: {'center_x': .5, 'top': .21}
            disabled: True if not root.Setup else False
        Button:
            text: "Connect"
            size_hint: 0.1, 0.08
            ## on_release: Factory.CalibratingPopup().open() if not root.Setup else None
            on_press: root.update_info() if app.do_setup(port_spinner.text, baud_spinner.text) else Factory.SetupPopup().open()
            on_release: app.startup()
            pos_hint: {'center_x': .5, 'top': .11}
            disabled: True if not root.Setup else False
        Label:
            size_hint: 0.1, 0.08
            text: "If Device Not Listed"
            font_name: 'fonts/JustMandrawn-0egd.ttf'
            font_size: root.height * 0.03
            pos_hint: {'top': .18, 'right': .141}
        Button:
            text: "Refresh Port List"
            size_hint: 0.1, 0.08
            on_release: port_spinner.values = app.available_ports()
            pos_hint: {'right': .14, 'top': .11}
            disabled: True if not root.Setup else False
        Label:
            text: "Connecting to the Transmitter"
            font_name: 'fonts/JustMandrawn-0egd.ttf'
            font_size: root.height * 0.161
            size_hint_y: 0.09
            pos_hint:{'top': .93}
        Label:
            text: "Select COM Port"
            font_name: 'fonts/JustMandrawn-0egd.ttf'
            font_size: root.height * 0.0852
            size_hint_y: 0.13
            pos_hint:{'top': .75, 'right': .83}
        Label:
            text: "Select Baudrate"
            font_name: 'fonts/JustMandrawn-0egd.ttf'
            font_size: root.height * 0.0852
            size_hint_y: 0.13
            pos_hint:{'top': .75, 'right': 1.23}
        Image:
            source: 'images/nano.png'
            size_hint: 0.39, 0.39
            pos_hint: {'center_x': .32, 'top': .51}
        Image:
            source: 'images/nrf.png'
            size_hint: 0.83, 0.83
            pos_hint: {'center_x': .72, 'top': .76}

    FloatLayout:
        opacity: 1 if not root.Setup else 0

        Button:
            id: btnAbort2
            text: "ABORT!!!"
            size_hint: 0.052, 0.05
            pos_hint: {'top': .93, 'right': .991}
            on_press: app.abort()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
            disabled: True if root.Setup else False

        GridLayout:
            rows: 1
            cols: 4
            row_default_height: 5
            size_hint_y: 0.15
            pos_hint: {'top': .35}

            Label:
                text: 'Throttle: Value is %s' % int(s1.value) if s1.value else 'Throttle: Not Set'
            Label:
                text: 'Yaw: Value is %s' % int(s2.value) if s2.value else 'Yaw: Not Set'
            Label:
                text: 'Pitch: Value is %s' % int(s3.value) if s3.value else 'Pitch: Not Set'
            Label:
                text: 'Roll: Value is %s' % int(s4.value) if s4.value else 'Roll: Not Set'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.11
            pos_hint: {'top': .29}

            Label:
                size_hint: (.18, 1)

            Slider:
                id: s1
                value: 0
                on_value: app.set_s1(int(self.value))
                range: (0,255)
                step: 1
                disabled: True if root.Setup else False

            Label:
                size_hint: (.35, 1)

            Slider:
                id: s2
                value: 0
                on_value: app.set_s2(int(self.value))
                range: (0,255)
                step: 1
                disabled: True if root.Setup else False
                
            Label:
                size_hint: (.35, 1)

            Slider:
                id: s3
                value: 0
                on_value: app.set_s3(int(self.value))
                range: (0,255)
                step: 1
                disabled: True if root.Setup else False

            Label:
                size_hint: (.35, 1)

            Slider:
                id: s4
                value: 0
                on_value: app.set_s4(int(self.value))
                range: (0,255)
                step: 1
                disabled: True if root.Setup else False

            Label:
                size_hint: (.15, 1)


        BoxLayout:
            size_hint: 0.08, 0.05
            pos_hint: {'center_x': .5, 'top': .58}
            Button:
                text: "Enter"
                disabled: True if root.Setup else False
                on_release: Factory.ValidPopup().open() if (app.do_directcheck(throttle_text.text, \
                yaw_text.text, pitch_text.text, roll_text.text, aux1.active, aux2.active)) else Factory.InvalidPopup1().open()

        BoxLayout:
            size_hint: 0.08, 0.05
            pos_hint: {'center_x': .5, 'top': .12}
            Button:
                text: "Enter"
                disabled: True if root.Setup else False
                on_release: Factory.ValidPopup().open() if app.do_rampcheck() else Factory.InvalidPopup2().open()

        BoxLayout:
            size_hint: 0.052, 0.05
            pos_hint: {'right': .991, 'top': .87}
            Button:
                text: "Help"
                disabled: True if root.Setup else False
                on_release: Factory.HelpPopup().open()
            
        Label:
            text: "Ramp Control"
            font_name: 'fonts/JustMandrawn-0egd.ttf'
            font_size: root.height * .14
            size_hint_y: 0.14
            pos_hint:{'top': .44}
        Label:
            text: "Instantaneous Control"
            font_name: 'fonts/JustMandrawn-0egd.ttf'
            font_size: root.height * .13
            size_hint_y: 0.07
            pos_hint:{'top': .93}

        GridLayout:
            rows: 1
            cols: 6
            row_default_height: 5
            size_hint_y: 0.14
            pos_hint: {'top': .80}

            Label:
                text: "Throttle"
            Label:
                text: "Yaw"
            Label:
                text: "Pitch"
            Label:
                text: "Roll"
            Label:
                text: "AUX1 (Arm)"
            Label:
                text: "AUX2 (Arm Acc)"

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: .10
            pos_hint: {'top': .74}

            Label:
                size_hint: (.22, 1)

            TextInput:
                id: throttle_text
                pos_hint: {'top': .63}
                size_hint: (.6, .267)
                height:30
                multiline: False
                disabled: True if root.Setup else False

            Label:
                size_hint: (.40, 1)

            TextInput:
                id: yaw_text
                pos_hint: {'top': .63}
                size_hint: (.6, .267)
                height:30
                multiline: False
                disabled: True if root.Setup else False
                
            Label:
                size_hint: (.40, 1)

            TextInput:
                id: pitch_text
                pos_hint: {'top': .63}
                size_hint: (.6, .267)
                height:30
                multiline: False
                disabled: True if root.Setup else False

            Label:
                size_hint: (.40, 1)

            TextInput:
                id: roll_text
                pos_hint: {'top': .63}
                size_hint: (.6, .267)
                height:30
                multiline: False
                disabled: True if root.Setup else False

            Label:
                size_hint: (.22, 1)

            Switch:
                id: aux1
                pos_hint: {'top': .98}
                active: False
                disabled: True if root.Setup else False

            Switch:
                id: aux2
                pos_hint: {'top': .98}
                active: False
                disabled: True if root.Setup else False

<DocView>:
    FloatLayout:
        Button:
            id: btnExit2
            text: "Exit"
            size_hint: 0.05, 0.05
            pos_hint: {'top': .99, 'right': .99}
            on_press: Factory.ExitPopup1().open() if not app.check_connect() else Factory.ExitPopup2().open()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        FloatLayout:
            size_hint: 1, .93
            RstDocument:
                text: root.text

<Check1Popup@Popup>:
    title: 'Value not defined.'
    size_hint: (0.2, 0.14)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Please select a port and baudrate."
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()

<Check2Popup@Popup>:
    title: 'Success.'
    size_hint: (0.2, 0.14)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "A valid port and baudrate has been selected!"
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()

<SetupPopup@Popup>:
    title: 'Unable to connect.'
    size_hint: (0.24, 0.14)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Please try again. Press the 'Check' button to verify first."
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()
            
<HelpPopup@Popup>:
    title: 'Understanding Quadrocopter Basics'
    size_hint: (0.2, 0.25)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Image:
            source: 'images/quad_basics.png'
        Button:
            size_hint: 0.2, 0.2
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()

<ValidPopup@Popup>:
    title: 'Valid Response'
    size_hint: (0.24, 0.14)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Valid response. Values have been changed successfully!"
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()

<InvalidPopup1@Popup>:
    title: 'Invalid Response'
    size_hint: (0.2, 0.14)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Please enter a valid value (0-255) for each signal."
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()
            
<InvalidPopup2@Popup>:
    title: 'Invalid Response'
    size_hint: (0.2, 0.14)
    size: (300, 150)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "At least one value (slider) must be set."
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()

<ExitPopup1@Popup>:
    title: 'Exit'
    size_hint: (0.15, 0.25)
    size: (300, 150)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Are you sure you want to quit?"
        Button:
            size_hint: 0.2, 0.5
            pos_hint: {'center_x': .5}
            text: 'Yes'
            on_release: app.stop()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Label:
            size_hint: 0.1, 0.1
        Button:
            size_hint: 0.5, 0.5
            pos_hint: {'center_x': .5}
            text: 'Disconnect Port'
            disabled: True
            on_release: app.disconnect()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Label:
            size_hint: 0.1, 0.1
        Button:
            size_hint: 0.2, 0.5
            pos_hint: {'center_x': .5}
            text: 'No'
            on_press: root.dismiss()

<ExitPopup2@Popup>:
    title: 'Exit'
    size_hint: (0.15, 0.25)
    size: (300, 150)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Are you sure you want to quit?"
        Button:
            size_hint: 0.2, 0.5
            pos_hint: {'center_x': .5}
            text: 'Yes'
            on_release: app.stop()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Label:
            size_hint: 0.1, 0.1
        Button:
            size_hint: 0.5, 0.5
            pos_hint: {'center_x': .5}
            text: 'Disconnect Port'
            disabled: False
            on_release: app.disconnect()
            background_normal: ''
            background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
        Label:
            size_hint: 0.1, 0.1
        Button:
            size_hint: 0.2, 0.5
            pos_hint: {'center_x': .5}
            text: 'No'
            on_press: root.dismiss()


<NumTargetsPopup@Popup>:
    title: 'Setting Targets'
    size_hint: (0.15, 0.20)
    auto_dismiss: False

    FloatLayout:
        Label:
            text: "Enter Number of Targets:"
            size_hint: .1, .1
            pos_hint: {'top': .9, 'center_x': 0.5}
        TextInput:
            id: num_targets
            size_hint: 0.2, 0.25
            pos_hint: {'top': .7, 'center_x': 0.5}
            multiline: False
            font_size: root.height * 0.09
        Button:
            text: "Enter"
            size_hint: 0.3, 0.3
            pos_hint: {'top': .37, 'center_x': 0.32}
            on_release: Factory.TargetPopup().open() if app.retrieveNumTargets(num_targets.text) != -1 else Factory.InvalidNumTargetsPopup().open()
            on_release: app.setnumtargets(num_targets.text)
            on_release: root.dismiss()
        Button:
            text: "Cancel"
            size_hint: 0.3, 0.3
            pos_hint: {'top': .37, 'center_x': 0.68}
            on_release: root.dismiss()

<InvalidNumTargetsPopup@Popup>:
    title: 'Invalid Value'
    size_hint: (0.2, 0.14)
    size: (300, 150)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label: 
            text: "Buy a better drone."
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()

<InvalidLatLongPopup@Popup>:
    title: 'Invalid Value'
    size_hint: (0.2, 0.14)
    size: (300, 150)
    auto_dismiss: False

    BoxLayout:
        orientation: 'vertical'
        Label: 
            text: "Each value must have exactly 6 decimal places."
        Button:
            size_hint: 0.2, 0.7
            pos_hint: {'center_x': .5}
            text: 'Close'
            on_release: root.dismiss()
    

<TargetPopup@Popup>:
    title: 'Number of targets is %s' % app.shownumtargets() if app.shownumtargets() else '0'
    id: target_popup
    size_hint: (0.5, 0.95)
    auto_dismiss: False
    FloatLayout:
        Label:
            id: num_label
            opacity: 0
            text: '%s' % app.shownumtargets() if app.shownumtargets() else '0'
        GridLayout:
            pos_hint: {'top': 1, 'center_x': 0.5}
            cols: 2
            rows: 16
            Label:
                text: 'Latitude'
                font_size: root.height * 0.05
                size_hint: 0.2, 0.2
            Label:
                text: 'Longitude'
                font_size: root.height * 0.05
                size_hint: 0.2, 0.2
            TextInput:
                id: target1_lat
                opacity: 1 if (num_label.text == '1' or num_label.text == '2' \
                                or num_label.text == '3' or num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target1_long
                opacity: 1 if (num_label.text == '1' or num_label.text == '2' \
                                or num_label.text == '3' or num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target2_lat
                opacity: 1 if (num_label.text == '2' \
                                or num_label.text == '3' or num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target2_long
                opacity: 1 if (num_label.text == '2' \
                                or num_label.text == '3' or num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target3_lat
                opacity: 1 if (num_label.text == '3' or num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target3_long
                opacity: 1 if (num_label.text == '3' or num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target4_lat
                opacity: 1 if (num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target4_long
                opacity: 1 if (num_label.text == '4' \
                                or num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target5_lat
                opacity: 1 if (num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target5_long
                opacity: 1 if (num_label.text == '5' or num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target6_lat
                opacity: 1 if (num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target6_long
                opacity: 1 if (num_label.text == '6' \
                                or num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target7_lat
                opacity: 1 if (num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target7_long
                opacity: 1 if (num_label.text == '7' or num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target8_lat
                opacity: 1 if (num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target8_long
                opacity: 1 if (num_label.text == '8' \
                                or num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target9_lat
                opacity: 1 if (num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target9_long
                opacity: 1 if (num_label.text == '9' or num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target10_lat
                opacity: 1 if (num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            TextInput:
                id: target10_long
                opacity: 1 if (num_label.text == '10') else 0
                size_hint: 0.08, 0.08
                pos_hint: {'top': 1, 'center_x': 0.5}
                multiline: False
                font_size: root.height * 0.045
            Button:
                size_hint: 0.2, 0.2
                pos_hint: {'center_x': .5}
                text: 'Enter'
                background_normal: ''
                background_color: 0.203125, 0.453125, 0.453125, 1
                on_press: app.load_gif()
                on_release: app.targets_sent()
                on_release: root.dismiss() if app.do_check_latlong(target1_long.text, target1_lat.text, \
                                                                target2_long.text, target2_lat.text, \
                                                                target3_long.text, target3_lat.text, \
                                                                target4_long.text, target4_lat.text, \
                                                                target5_long.text, target5_lat.text, \
                                                                target6_long.text, target6_lat.text, \
                                                                target7_long.text, target7_lat.text, \
                                                                target8_long.text, target8_lat.text, \
                                                                target9_long.text, target9_lat.text, \
                                                                target10_long.text, target10_lat.text) else Factory.InvalidLatLongPopup().open()
            Button:
                size_hint: 0.2, 0.2
                pos_hint: {'center_x': .5}
                text: 'Go Back'
                background_normal: ''
                background_color: 0.85098039215, 0.32549019607, 0.30980392156, 1
                on_release: Factory.NumTargetsPopup().open()
                on_press: root.dismiss()

<CalibratingPopup@Popup>:
    id: calibratePopup
    title: "Calibrate Drone..."
    size_hint: (1, 1)
    auto_dismiss: False
    FloatLayout:
        Image:
            source: 'images/calibrate.png'
            size_hint: (1,1)
            pos_hint: {'center_y': .5, 'center_x': .5}
        Button:
            id: btnCalibrate
            size_hint: 1, 1
            pos_hint: {'center_y': .59, 'center_x': .495}
            text: ""
            on_press: app.startup()
            on_press: calibratePopup.title = "Calibrating Drone..."
            on_press: abortCalibration.disabled = False
            on_release: root.dismiss(53)
            background_normal: ''
            background_color: 0, 0.35686274509, 0.58823529411, 0
        Button:
            id: abortCalibration
            size_hint: 0.2, 0.08
            pos_hint: {'top': .63, 'right': 0.6}
            text: "Click here to ABORT!!!"
            on_press: app.abort()
            background_normal: ''
            background_color: 1, 1, 1, 0
            font_size: '24pt'
            color: 0.85098039215, 0.32549019607, 0.30980392156, 1
            disabled: True
        Label:
            text: 'Click Anywhere'
            font_name: 'fonts/Gilberto.ttf'
            font_size: root.height*0.20
            pos_hint: {'center_y': .89, 'center_x': .53}
"""
)

class ControllerView(Screen):
    Setup = BooleanProperty('True')
    def __init__(self,**kwargs):
        super(ControllerView, self).__init__(**kwargs)
##        Clock.schedule_interval(self., 1)
        
    def update_info(self):
        self.Setup = False

    def is_setup(self, dt):
        pass
##        if not self.Setup:
##            pop = root.create_popup()
##            pop.open()
##            pop.dismiss(1)

class DroneView(Screen):
    def __init__(self,**kwargs):
        super(DroneView, self).__init__(**kwargs)

class DroneAdvView(Screen):
    def __init__(self,**kwargs):
        super(DroneAdvView, self).__init__(**kwargs)
        # Exactly ONE of the below two lines should be commented
        ############################################
        self.vcap = None
        #self.vcap = cv2.VideoCapture('rtsp://Drimages:Satan666@192.168.1.20:554/live/ch1')
        #self.vcap = cv2.VideoCapture('rtsp://Drimages:Satan666@192.168.0.172:554/live/ch1')
        ############################################
        self.audio_start = True
        Clock.schedule_interval(self.update_pic, 0.01)
        self.thread = threading.Thread(target = self.stream_update, args=())
        self.thread.start()
        self.count = 0

    def update_pic(self, dt):
##        try:
##            Image.open("Gmap/drone_path.png")
##        except:
##            pass
##        else:

        gc.collect()
        
        self.ids.mapImage.reload()
        self.ids.prescoreImage.reload()
        self.ids.scoreImage.reload()
        self.ids.audio.volume = Speech.audio()

        if self.vcap != None:
            self.ret, self.frame = self.vcap.read()
            buf1 = cv2.flip(self.frame, 0)
            if buf1 is not None:
                buf = buf1.tostring()
                texture1 = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.ids.myexport.texture = texture1
                self.count += 1

    ##            print("Hello\n")
                if self.count % 30 == 1:
                    t = threading.Thread(target = self.anything_really, args = (self.frame, ))
                    t.start()
                #with concurrent.futures.ThreadPoolExecutor() as executor:
                    #future = executor.submit(self.anything_really, frame)
                    #future_result = future.result()
#self.ids.audio.volume = 1
    def stream_update(self):
        if self.audio_start:
            time.sleep(0.2)
            #self.ids.audio.source = 'rtsp://Drimages:Satan666@192.168.0.172:554/live/ch1'
            self.audio_start = False
        if self.vcap != None:
            if self.vcap.isOpened():
                self.ret, self.frame = self.vcap.read()
##        time.sleep(0.1)

    def anything_really(self, frame):
        score = str(ImageProcessing.process_image(frame))
        if score == "0" or score == "None" or score == "ERROR":
            score = "0.000000000000000"
        self.ids.score_label.text = "Score: " + score
        return True
            
class DocView(Screen):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_dir = "Documentation\Intro.rst"
    file_path = os.path.join(current_dir, relative_dir)
    text = ""
    with open(file_path) as fobj:
        for line in fobj:
            text += line
