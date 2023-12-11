import pandas as pd
from ipywidgets import widgets
from config import DataConfig


def reset_cbox(button, cbox):
    cbox.value = ''
