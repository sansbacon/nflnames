# nflnames/tests/test_nflnames_teams.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License


import random
import pytest

import nflnames
from nflnames import *


def test_TEAM_CODES():
    """tests TEAM_CODES"""
    assert isinstance(TEAM_CODES, dict)
    rkey = random.choice(list(TEAM_CODES.keys()))
    ritem = TEAM_CODES[rkey]
    assert isinstance(ritem, list)
    assert isinstance(random.choice(ritem), str)


def test_TEAM_NAMES():
    """tests TEAM_NAMES"""
    assert isinstance(TEAM_NAMES, dict)
    rkey = random.choice(list(TEAM_NAMES.keys()))
    ritem = TEAM_NAMES[rkey]
    assert isinstance(ritem, list)
    assert isinstance(random.choice(ritem), str)


def test_standardize(tprint):
    val = nflnames.teams._standardize(random.choice(list(TEAM_CODES.keys())), TEAM_CODES)
    assert isinstance(val, list)
    assert isinstance(val[0], tuple)
    assert isinstance(val[0][0], str)


def test_is_standardized():
    tc = 'gbp'
    assert not is_standardized({tc})
    assert is_standardized({standardize_team_code(tc)})


def test_standard_team_codes():
    assert isinstance(standard_team_codes(), set)


def test_standard_team_names():
    assert isinstance(standard_team_names(), set)


def test_standardize_team_code():
    tc = 'gbp'
    assert not is_standardized({tc})
    tcs = standardize_team_code(tc)
    assert is_standardized({tcs})
    

def test_standardize_team_name(tprint):
    tn = 'Texans'
    assert not is_standardized({tn})
    stn = standardize_team_name(tn)
    tprint(stn)
    assert is_standardized({stn}, team_type='name')

