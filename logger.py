import datetime
import os


log_filename = None


if not os.path.exists("logs"):
    os.makedirs("logs")


def initialize_logging():
    global log_filename
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_filepath = os.path.join("logs", log_filename)
    return log_filepath


def log_event(message, log_textbox=None):
    global log_filename
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}]: {message}"

    log_filepath = os.path.join("logs", log_filename)
    with open(log_filepath, "a") as log_file:
        log_file.write(log_message + "\n")

    if log_textbox:
        log_textbox.insert("end", log_message + "\n")
        log_textbox.yview_moveto(1)
