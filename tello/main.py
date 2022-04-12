import cv2
from threading import Thread
from termcolor import colored

from tello import sdk
from action import action
from interaction import keyboard
from interaction import view

drone = sdk.Tello('', 8889)
act = action.Action(drone)
view = view.View(drone)
keyboard = keyboard.Keyboard(drone, act, view)


print("research start")

while True:
    pass