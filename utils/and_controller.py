import os
import subprocess
from utils.cmd import print_with_color
import utils.constant as constant
import re


appPackage = constant.appPackage
appActivity = constant.appActivity


def execute_adb(adb_command):
    print(adb_command)
    
    result = subprocess.run(
        adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # print(result)
    if result.returncode == 0:
        return result.stdout.strip()
    print_with_color(f"Command execution failed: {adb_command}", "red")
    print_with_color(result.stderr, "red")
    return "ERROR"


def list_all_devices():
    adb_command = "adb devices"
    device_list = []
    result = execute_adb(adb_command)

    if result != "ERROR":
        devices = result.split("\n")[1:]
        for d in devices:
            device_list.append(d.split()[0])

    return device_list


class AndroidController:
    def __init__(self):
        self.device = constant.configs["DEVICE"]
        self.screenshot_dir = constant.configs["ANDROID_SCREENSHOT_DIR"]
        self.xml_dir =constant.configs["ANDROID_XML_DIR"]
        self.width, self.height = self.get_device_size()
        self.savedir = constant.savedir
        self.backslash = "\\"

    def get_device_size(self):
        adb_command = f"adb -s {self.device} shell wm size"
        result = execute_adb(adb_command)
        if result != "ERROR":
            return map(int, result.split(": ")[1].split("x"))
        return 0, 0

    def get_screenshot(self,path):
        cap_command = f"adb -s {self.device} shell screencap -p " \
                      f"{os.path.join(self.screenshot_dir,'tmp.png')}"
        pull_command = f"adb -s {self.device} pull " \
                       f"{os.path.join(self.screenshot_dir,'tmp.png')} " \
                       f"{path}"
        result = execute_adb(cap_command)
        if result != "ERROR":
            result = execute_adb(pull_command)
            if result != "ERROR":
                return os.path.join(self.savedir)
            return result
        return result

    def get_xml(self,path):
        dump_command = f"adb -s {self.device} shell uiautomator dump " \
                       f"{os.path.join(self.xml_dir,'tmp.xml' )}"
        pull_command = f"adb -s {self.device} pull " \
                       f"{os.path.join(self.xml_dir,'tmp.xml' )} " \
                       f"{path}"

        result = execute_adb(dump_command)
        if result != "ERROR":
            result = execute_adb(pull_command)
            if result != "ERROR":
                return os.path.join(self.savedir + ".xml")
            return result
        return result

    def back(self):
        adb_command = f"adb -s {self.device} shell input keyevent KEYCODE_BACK"
        ret = execute_adb(adb_command)
        return ret

    def stop_app(self):
        adb_command = f"adb -s {self.device} shell am force-stop {appPackage}"
        ret = execute_adb(adb_command)
        return ret

    def start_app(self):
        adb_command = f"adb -s {self.device} shell am start -n {appPackage}/{appActivity}"
        ret = execute_adb(adb_command)
        return ret

    def home(self):
        adb_command = f"adb -s {self.device} shell input keyevent 3"
        ret = execute_adb(adb_command)
        return ret

    def tap(self, tl, br):
        x, y = (tl[0] + br[0]) // 2, (tl[1] + br[1]) // 2
        adb_command = f"adb -s {self.device} shell input tap {x} {y}"
        ret = execute_adb(adb_command)
        return ret

    def tap_point(self, x: float, y: float):
        x = int(x * self.width)
        y = int(y * self.height)
        adb_command = f"adb -s {self.device} shell input tap {x} {y}"
        ret = execute_adb(adb_command)
        return ret

    def text(self, input_str):
        input_str = input_str.replace(" ", "%s")
        input_str = input_str.replace("'", "")
        adb_command = f"adb -s {self.device} shell input text {input_str}"
        ret = execute_adb(adb_command)
        return ret

    def long_press(self, tl, br, duration=1000):
        x, y = (tl[0] + br[0]) // 2, (tl[1] + br[1]) // 2
        adb_command = f"adb -s {self.device} shell input swipe {x} {y} {x} {y} {duration}"
        ret = execute_adb(adb_command)
        return ret

    def long_press_point(self, x: float, y: float, duration=1000):
        x = int(x * self.width)
        y = int(y * self.height)
        adb_command = f"adb -s {self.device} shell input swipe {x} {y} {x} {y} {duration}"
        ret = execute_adb(adb_command)
        return ret

    def swipe(self, tl, br, direction, dist="short", quick=False):
        unit_dist = int(self.width / 10)
        if dist == "long":
            unit_dist *= 3
        elif dist == "medium":
            unit_dist *= 2
        x, y = (tl[0] + br[0]) // 2, (tl[1] + br[1]) // 2
        if direction == "up":
            offset = 0, -2 * unit_dist
        elif direction == "down":
            offset = 0, 2 * unit_dist
        elif direction == "left":
            offset = -1 * unit_dist, 0
        elif direction == "right":
            offset = unit_dist, 0
        else:
            return "ERROR"
        duration = 100 if quick else 400
        adb_command = f"adb -s {self.device} shell input swipe {x} {y} {x+offset[0]} {y+offset[1]} {duration}"
        ret = execute_adb(adb_command)
        return ret

    def swipe_point(self, start, end, duration=400):
        start_x, start_y = int(
            start[0] * self.width), int(start[1] * self.height)
        end_x, end_y = int(end[0] * self.width), int(end[1] * self.height)
        adb_command = f"adb -s {self.device} shell input swipe {start_x} {start_x} {end_x} {end_y} {duration}"
        ret = execute_adb(adb_command)
        return ret

    def get_info(self):
        adb_command = f"adb -s {self.device} shell dumpsys window | grep mFocusedApp"
        ret = execute_adb(adb_command)
        print(ret)
        activites = ret.split('\n')
        for key in activites:
            key = key.strip()
            if(constant.appPackage in key):
                match = re.search(r'(\S+)/(\S+)\s', key)
                if match:
                    app_name, activity_name = match.groups()
                    print(f"App 名称: {app_name}")
                    print(f"活动名称: {activity_name}")
                return [app_name,activity_name]
            else:
                return None
