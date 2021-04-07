#!/usr/bin/python


from __future__ import unicode_literals
import pytest
import os
import logging
from monitor import vmstatAddValue


vmstat = """procs -----------memory---------- ---swap-- -----io---- -system-- ----cpu----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa
 0  0      0  14720   2048  57092    0    0     0     0   12    7  2  3 95  0
"""

def test_VMStat():
    row = {}
    vmstatAddValue(vmstat, row, "VMSTAT", True)
    assert row['VMSTAT-bi'] == 0