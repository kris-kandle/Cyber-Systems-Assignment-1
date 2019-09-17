# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:48:44 2019

@author: krist
"""

import xmltodict
import sys

with open('C:\\Users\\krist\\OneDrive\\Skrivebord\\CyberSystems\\fsmd-sim\\test_1\\test_desc.xml') as fd:
    test_1 = xmltodict.parse(fd.read())
with open('C:\\Users\\krist\\OneDrive\\Skrivebord\\CyberSystems\\fsmd-sim\\test_2\\gcd_desc.xml') as fd1:
    test_2_desc = xmltodict.parse(fd1.read())
with open('C:\\Users\\krist\\OneDrive\\Skrivebord\\CyberSystems\\fsmd-sim\\test_2\\gcd_stim.xml') as fd2:
    test_2_stim = xmltodict.parse(fd2.read())
