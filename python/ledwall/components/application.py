from ..components.event import *
from ..util import TimeDelta
from ..components import Display


class Application(object):

    def __init__(self, display, framerate):
        # type : (Display) -> None
        self._display = display
        self._display.fill((0,0,0))
        self._display.update()
        self._framerate = framerate
        self._running = True
        self._event_dispatcher = EventDispatcher()
        if framerate and framerate > 0:
            self._event_dispatcher.add_emitter(FramerateEmitter(framerate))

        self._event_dispatcher.add_emitter(GamepadEmitter())            

    @property
    def display(self):
        return self._display

    @property
    def frame(self):
        return self.display.frame

    def add_emitter(self,emitter):
        #self._event_dispatcher.add_emitter(emitter)
        self._event_dispatcher += emitter
        
    def paint(self):
        pass

    def handle_event(self, event):
        pass

    def start_loop(self):
        try:
            while self._running:
                event = self._event_dispatcher.next_event()
                if (event.type, event.action) == (Event.SYSTEM,'update'):
                    self.update()
                else:
                    self.handle_event(event)
        except KeyboardInterrupt:
            self.stop_loop()
            print("\nGood Buy")
            print("May the force be with you ...")

    def stop_loop(self):
        self._running = False
        self._event_dispatcher.stop()

    def update(self):
        self.paint()
        try:
            #self._event_dispatcher.suspend()            
            self._display.update()
        finally:
            #self._event_dispatcher.resume()            
            pass

class SmileApplication(Application):
    def __init__(self, sender, framerate):
        super().__init__(Display(10, 10, sender, mode=Display.MODE_ZIGZAG), framerate)
        self.action_map = {
            (Event.GAMEPAD, 'ABS_X', 0)       : self.btn_left_pressed,
            (Event.GAMEPAD, 'ABS_X', 255)     : self.btn_right_pressed,
            (Event.GAMEPAD, 'ABS_Y', 0)       : self.btn_top_pressed,
            (Event.GAMEPAD, 'ABS_Y', 255)     : self.btn_down_pressed,
            (Event.GAMEPAD, 'BTN_THUMB', 1)   : self.btn_a_pressed,
            (Event.GAMEPAD, 'BTN_THUMB2', 1)  : self.btn_b_pressed,
            (Event.GAMEPAD, 'BTN_PINKIE', 1)  : self.btn_r_pressed,
            (Event.GAMEPAD, 'BTN_TOP2', 1)    : self.btn_l_pressed,
            (Event.GAMEPAD, 'BTN_TRIGGER', 1) : self.btn_x_pressed,
            (Event.GAMEPAD, 'BTN_TOP', 1)     : self.btn_y_pressed,
            (Event.GAMEPAD, 'BTN_BASE3', 1)   : self.btn_select_pressed,
            (Event.GAMEPAD, 'BTN_BASE4', 1)   : self.btn_start_pressed,
            (Event.GAMEPAD, 'ABS_Y',   127)   : self.btn_abs_y_released,
        }

    def handle_event(self, event):
        action = self.action_map.get((event.type,event.action,event['state']),None)
        if action:
            action()

    def set_action(self, source, action_name, state, action):
        old_action = self.action_map.get((source, action_name, state))
        self.action_map[(source, action_name, state)] = action
        return old_action
        
    def btn_a_pressed(self):
        pass
    
    def btn_b_pressed(self):
        pass

    def btn_x_pressed(self):
        pass

    def btn_y_pressed(self):
        pass

    def btn_r_pressed(self):
        pass

    def btn_l_pressed(self):
        pass

    def btn_up_pressed(self):
        pass

    def btn_down_pressed(self):
        pass

    def btn_top_pressed(self):
        pass

    def btn_abs_y_released(self):
        pass
    
    def btn_left_pressed(self):
        pass

    def btn_right_pressed(self):
        pass

    def btn_select_pressed(self):
        pass

    def btn_start_pressed(self):
        pass
    
