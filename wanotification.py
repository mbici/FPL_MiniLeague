import time
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()


def send_whatsapp_message(msg: str, groupId: str):
    try:
        pywhatkit.sendwhatmsg_to_group_instantly(
            group_id=groupId,
            message=msg,
            wait_time=20
        )
        time.sleep(10)
        pyautogui.click()
        #time.sleep(2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Message sent!")
    except Exception as e:
        print(str(e))



if __name__ == "__main__":
    send_whatsapp_message(msg="Test message from a Python script!")