import json
import random
from collections import deque
from pynput import keyboard
import time

with open("uwu_config.json") as f:
    config = json.load(f)

replacements = config.get("replacements", {"l": "w", "r": "w"})
stutter_chance = config.get("stutter_chance", 0.2)
suffixes = config.get("suffixes", [" owo", " uwu", " >_<", " ^_^"])

last_keys = deque(maxlen=20)
kb = keyboard.Controller()
ignore = False

PUNCTUATION = set(".!?;:,")
SENTENCE_END = set(".!?")

def press_backspace(n=1):
    global ignore
    ignore = True
    for _ in range(n):
        kb.press(keyboard.Key.backspace)
        kb.release(keyboard.Key.backspace)
    ignore = False

def type_text(text):
    global ignore
    ignore = True
    for c in text:
        kb.press(c)
        kb.release(c)
    ignore = False

def type_key(key):
    global ignore
    ignore = True
    kb.press(key)
    kb.release(key)
    ignore = False

patterns = []
for k, v in replacements.items():
    patterns.append((k, v))
    patterns.append((k.upper(), v.upper()))

patterns.sort(key=lambda x: -len(x[0]))

def on_press(key):
    global ignore

    if ignore:
        return

    try:
        char = key.char
    except AttributeError:
        char = None

    if key == keyboard.Key.enter:
        char = "\n"

    if key == keyboard.Key.space:
        char = " "

    if not char:
        return

    last_keys.append(char)

    current_string = "".join(last_keys)
  
    for search, replace in patterns:
        if current_string.endswith(search):
            # IMPORTANT: erase FIRST
            press_backspace(len(search))
            time.sleep(0.04*len(search))
            # THEN type replacement
            type_text(replace)

            # Update buffer to match replacement
            for _ in range(len(search)):
                last_keys.pop()
            for c in replace:
                last_keys.append(c)
            break

    if len(last_keys) >= 2:
        prev = last_keys[-2]
        curr = last_keys[-1]
        if prev == " ":
            if random.random() < stutter_chance and curr.isalpha():
                type_text(f"-{curr}")
                last_keys.append("-")
                last_keys.append(curr)

    if char in SENTENCE_END or char == "\n":
        suffix = random.choice(suffixes)

        press_backspace(1)

        time.sleep(0.05)

        type_text(" " + suffix)

        if char == "\n":
            type_key(keyboard.Key.enter)
        else:
            type_text(char)

        last_keys.append(" ")
        for c in suffix:
            last_keys.append(c)
        last_keys.append(char)

def main():
    print("UwUifier (replace-as-you-type) running... Ctrl+C to stop")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
