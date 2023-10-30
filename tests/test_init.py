#!/usr/bin/python
# -*- coding: UTF-8 -*-

import oggmap


def test_title():
    assert oggmap.__title__ == 'oggmap'


def test_version():
    assert oggmap.__version__ == '0.0.1'


def test_license():
    assert oggmap.__license__ == 'GPL-3'
