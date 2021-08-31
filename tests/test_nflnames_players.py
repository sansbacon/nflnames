# nflnames/tests/test_nflnames_players.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

from nflnames import *
import pytest


def test_match_name():
    """Tests match name"""
    s = 'Odell Beckham Jr.'
    l = ['Odell Beckham', 'Odie McDowell']
    match = match_name(s, l)
    assert match[0] == 'Odell Beckham'
    assert match[1] > 80


def test_rearrange_name():
    """Tests rearrange_name"""
    s = 'Beckham Jr., Odell'
    assert rearrange_name(s) == 'Odell Beckham Jr.'


def test_remove_chars():
    """Tests remove_chars"""
    s = 'Odell Beckham Jr.'
    assert remove_chars(s) == 'Odell Beckham Jr'
    s = "Le'Veon Bell"
    assert remove_chars(s) == 'LeVeon Bell'


def test_remove_suffixes():
    """Tests remove_suffixes"""
    s = 'Odell Beckham, Jr.'
    assert remove_suffixes(s) == 'Odell Beckham, Jr.'
    assert remove_suffixes(remove_chars(s)) == 'Odell Beckham'


def test_standardize_defense_name():
    #(s: str) -> str:
    #"""Standardizes DST name
    s = "San Francisco 49ers"
    assert standardize_defense_name(s) == '49ers defense'


def test_standardize_player_name():
    s = 'Henry Ruggs IV'
    assert standardize_player_name(s) == 'henry ruggs'


def test_standardize_positions():
    for s in ('DST', 'Defense', 'def'):
        assert standardize_positions(s) == 'DST'
    assert standardize_positions('qb') == 'qb'

