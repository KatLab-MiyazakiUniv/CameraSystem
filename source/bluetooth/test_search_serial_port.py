"""
@file: test_search_serial_port.py
@author: Futa HIRAKOBA
@brief: search_serial_port.pyのをテストするプログラム
"""

from search_serial_port import search_com_ports, search_enabled_com_port


def test_search_com_ports():
    search_com_ports()


def test_search_enabled_com_port():
    search_enabled_com_port()
