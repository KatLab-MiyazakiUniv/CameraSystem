"""
@file: test_Bluetooth.py
@author: Futa HIRAKOBA
@brief: Bluetooth.pyのをテストするプログラム
"""

import pytest
import serial
from Bluetooth import Bluetooth


@pytest.fixture()
def bluetooth():
    return Bluetooth()


def test_create():
    Bluetooth()
