# -*- coding: utf-8 -*-
# tests/test_db.py
from nflnames.players import normalize_name
import pandas as pd
import pytest

from nflnames import defense_to_dst, fix_name


def test_defense_to_dst():
    """Tests defense_to_dst"""
    col = pd.Series(['Def', 'Def', 'QB'])
    assert defense_to_dst(col).equal(pd.Series(['DST', 'DST', 'QB']))


def test_normalize_name():
    """Tests normalize_name"""
    pairs = (('Smith Jr., Dennis', 'smith dennis'),
             ('Greenv, V.J.', 'greenv vj'),
             ('Giants, New York', 'giants new york'),
             ('Fuller V, Will', 'fuller will'),
             ('Robinson IV, Nate', 'robinson nate'),
            )
    
    for old, new in pairs:
        assert normalize_name(old) == new


def test_fix_name():
    """Tests fix_name"""
    names = ['Smith Jr., J.R.', 'Bills, Buffalo', 'Brady, Tom']
    pos = ['WR', 'DST', 'QB']
    df = pd.DataFrame({'position': pos, 'name_': names})
    df['name_norm'] = df.apply(fix_name, axis=1)
    newnames = df.loc[:, 'name_norm'].values.tolist()
    assert newnames == ['jr smith', 'bills defense', 'tom brady']

    # test column arg
    names = ['Smith Jr., J.R.', 'Bills, Buffalo', 'Brady, Tom']
    pos = ['WR', 'DST', 'QB']
    df = pd.DataFrame({'position': pos, 'name_norm': names})
    df['name_norm'] = df.apply(fix_name, args=('name_norm', ), axis=1)
    newnames = df.loc[:, 'name_norm'].values.tolist()
    assert newnames == ['jr smith', 'bills defense', 'tom brady']