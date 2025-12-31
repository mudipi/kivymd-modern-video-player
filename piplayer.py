from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.slider import MDSlider
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from gradient import *

# registering our new custom fontstyle
LabelBase.register(name='SF-Pro', fn_regular='font/Montserrat-Medium.ttf')

Builder.load_file('piplayer.kv')

#----------- ############## ------------

class PiPlayerContainer(MDGridLayout):
    video = ObjectProperty(None)

class PiControlsTopBox(MDFloatLayout):
    video = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shader_widget = ShaderWidget(fs=GLSL_CODE)
        self.add_widget(self.shader_widget)

class PiControlsBottomBox(MDFloatLayout):
    video = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shader_widget = ShaderWidget(fs=GLSL_CODE)
        self.add_widget(self.shader_widget)

class PiControlsBox(MDGridLayout):
    video = ObjectProperty(None)

class PiSliderBox(MDBoxLayout):
    video = ObjectProperty(None)

class PiPlayerButtons(MDBoxLayout):
    video = ObjectProperty(None)

#----------- Custom Slider -----------

class PiProgressBarVideo(MDSlider):
    video = ObjectProperty(None)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        self._update_seek(touch.x)

    def _update_seek(self, x):
        if self.width == 0:
            return
        x = max(self.x, min(self.right, x)) - self.x
        self.video.seek(x / float(self.width))

#--------- Custom Control Buttons ---------

class PiBaseButtons(MDIconButton):
    video = ObjectProperty(None)
    clock = ObjectProperty()
    _fwd_position = NumericProperty(0)
    _bwd_position = NumericProperty(0)
    theme_icon_color = "Custom"
    icon_color = "white"
    icon_size = sp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock = None

class ButtonControlsLock(PiBaseButtons):
    locked = BooleanProperty(False)  # Define a Boolean property to track state

class ButtonControlsVolume(PiBaseButtons):
    volume = BooleanProperty(False)  # Define a Boolean property to track state

class ButtonRewindFiveSecondsBack(PiBaseButtons):
    def rewind_5s(self):
        if self.clock:
            self.clock.cancel()
        if self._bwd_position > self.video.position or self._bwd_position == 0:
            new_position = max(self.video.position - 5, 0)
            self._bwd_position = new_position
        else:
            self._bwd_position = new_position = self._bwd_position - 5
        duration = self.video.duration
        self.video.seek(new_position / duration)
        self.clock = Clock.schedule_once(lambda _: self.clock(), 2)

class ButtonRewindFiveSecondsForward(PiBaseButtons):
    def forward_5s(self):
        if self.clock:
            self.clock.cancel()
        if self._fwd_position < self.video.position:
            new_position = min(self.video.position + 5, self.video.duration)
            self._fwd_position = new_position
        else:
            self._fwd_position = new_position = self._fwd_position + 5
        duration = self.video.duration
        self.video.seek(new_position / duration)
        self.clock = Clock.schedule_once(lambda _: self.clock(), 2)

class ButtonRewindBack(PiBaseButtons):
    pass

class ButtonRewindForward(PiBaseButtons):
    pass

class ButtonVideoPlayPause(PiBaseButtons):
    def on_release(self, *args):
        if self.video.state == 'play':
            self.video.state = 'pause'
        else:
            self.video.state = 'play'

class ButtonDawnload(PiBaseButtons):
    pass

class ButtonExitAndFullScreen(PiBaseButtons):
    pass

class PiVideoPlayer(Video):
    '''Implement a custom video player.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_time(self):
        '''Set the timeline of the current playback with start and end times'''
        
        seek = self.position / self.duration
        elapsed_time = self.duration * seek
        remaining_time = self.duration - elapsed_time

        # Calculate hours, minutes, seconds for elapsed (start) time
        start_hours = int(elapsed_time // 3600)
        start_minutes = int((elapsed_time % 3600) // 60)
        start_seconds = int(elapsed_time % 60)

        # Calculate hours, minutes, seconds for remaining (end) time
        end_hours = int(remaining_time // 3600)
        end_minutes = int((remaining_time % 3600) // 60)
        end_seconds = int(remaining_time % 60)

        # Update start_time and end_time labels
        self.ids.button_box.ids.start_time.text = "%02d:%02d:%02d" % (start_hours, start_minutes, start_seconds)
        self.ids.button_box.ids.end_time.text = "%02d:%02d:%02d" % (end_hours, end_minutes, end_seconds)

class MainApp(MDApp):
    title = "Pi Video Player"

    def build(self):
        player = PiVideoPlayer(
            source="videos/Marvel_Studios_Doctor_Strange_Trailer.mp4",
            state='play',
            options={'allow_stretch': True},
            allow_stretch=True,
            volume=0.1,
            keep_ratio=False,
        )
        return player

if __name__ == '__main__':
    MainApp().run()
