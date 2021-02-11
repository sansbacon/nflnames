import pytest


from nflnames import standardize_team_code, standardize_team_name


def test_get_team_code():
    """Test get team code"""
    team_code = 'BAL'
    assert standardize_team_code('rav') == team_code
    assert standardize_team_code('RAV') == team_code
    assert standardize_team_code('bal') == team_code
    assert standardize_team_code('ravens') == team_code
    with pytest.raises(ValueError):
        standardize_team_code('xanadu')
        
        
def test_standardize_team_name():
    """Test standardize team name"""
    team_name = 'Baltimore Ravens'
    assert standardize_team_name('rav') == team_name
    assert standardize_team_name('RAV') == team_name
    assert standardize_team_name('bal') == team_name
    assert standardize_team_name('ravens') == team_name
    with pytest.raises(ValueError):
        standardize_team_name('xanadu')

