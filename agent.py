# w/ help from luc on SO: https://stackoverflow.com/questions/2090464/python-window-activation

from mnk.keyboard_emulator import PressKey, ReleaseKey, VK_LEFT, VK_RIGHT, VK_UP, VK_DOWN, VK_RETURN, VK_ESCAPE
import win32gui
import re
import time

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

class Agent:

    def __init__(self):
        """Constructor"""
        self.wmgr = WindowMgr()

    def refocus(self):
        self.wmgr = WindowMgr()
        self.wmgr.find_window_wildcard(".*Buckshot.*")
        self.wmgr.set_foreground()

    def new_episode(self):
        self.refocus()

        time.sleep(5)

        print("Going to main menu...")
        # go to main menu
        PressKey(VK_ESCAPE)
        time.sleep(3)
        ReleaseKey(VK_ESCAPE)

        time.sleep(10)

        print("Selecting `Start`...")
        # select "start"
        PressKey(VK_UP)
        ReleaseKey(VK_UP)
        time.sleep(0.25)
        PressKey(VK_DOWN)
        ReleaseKey(VK_DOWN)
        time.sleep(0.25)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)

        time.sleep(12)

        print("Selecting pills...")
        # select pills
        PressKey(VK_LEFT)
        ReleaseKey(VK_LEFT)
        time.sleep(0.5)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)

        time.sleep(5)
        
        print("Selecting `Yes`...")
        # select "yes"
        PressKey(VK_LEFT)
        ReleaseKey(VK_LEFT)
        time.sleep(0.5)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)

        time.sleep(5)

        print("Kicking First Door...")
        # kick first door
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)

        time.sleep(5)

        print("Kicking Second Door...")
        # kick second door
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)

        time.sleep(15)
        
        print("Picking up the waiver...")
        # pick up waiver
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)

        time.sleep(5)

        # sign "name"
        # b
        PressKey(VK_RIGHT)
        ReleaseKey(VK_RIGHT)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)
        time.sleep(0.25)

        # o
        for _ in range(4):
            PressKey(VK_DOWN)
            ReleaseKey(VK_DOWN)
            time.sleep(0.1)
        for _ in range(2):
            PressKey(VK_RIGHT)
            ReleaseKey(VK_RIGHT)
            time.sleep(0.1)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)
        time.sleep(0.25)

        # t
        for _ in range(2):
            PressKey(VK_DOWN)
            ReleaseKey(VK_DOWN)
            time.sleep(0.1)
        for _ in range(3):
            PressKey(VK_LEFT)
            ReleaseKey(VK_LEFT)
            time.sleep(0.1)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)
        time.sleep(0.25)

        # <enter>
        for _ in range(4):
            PressKey(VK_UP)
            ReleaseKey(VK_UP)
            time.sleep(0.1)
        for _ in range(2):
            PressKey(VK_RIGHT)
            ReleaseKey(VK_RIGHT)
            time.sleep(0.1)
        PressKey(VK_RETURN)
        ReleaseKey(VK_RETURN)
        time.sleep(0.25)




if __name__ == "__main__":
    agent = Agent()
    agent.new_episode()
