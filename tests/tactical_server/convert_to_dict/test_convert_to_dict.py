from tactical_server.sections.convert_to_dict import convert_to_dict
import pytest

TEST_DATA = [
    (
        "id:1,Ident:1",
        ({'id': 1, 'Ident': "1"})
    ),
    (
        "id:1,HR:67",
        ({'id': 1, 'HR': 67})
    ),
    (
        "id:862097,lat:52.65913,long:-8.62513",
        ({'id': 862097, 'lat': '52.65913', 'long': '-8.62513'})
    ),
    (
        "id:1,Rndsfired:5,RifleBat:98",
        ({'id': 1, 'Rndsfired': 5, 'RifleBat': '98'})
    ),
    (
        "id:1,State:1,ArmourBat:80",
        ({'id': 1, 'State': '1', 'ArmourBat': '80'})
    ),
    (
        "id:1,State:0,ArmourBat:60",
        ({'id': 1, 'State': '0', 'ArmourBat': '60'})
    ),
    (
        "id:1,lat:52.66206,long:-8.20898",
        ({'id': 1, 'lat': "52.66206", 'long': '-8.20898'})
    )
]


@pytest.mark.parametrize("message, expected_result", TEST_DATA)
def test_convert_to_dict( message, expected_result):
    result = convert_to_dict(message)

    assert result == expected_result



# coverage run --source=/home/tiege/code_portfolio/section-monitoring-system/tactical_server/convert_to_dict/ -m pytest /home/tiege/code_portfolio/section-monitoring-system/tests/tactical_server/convert_to_dict/ --ignore=/home/tiege/code_portfolio/section-monitoring-system/tests/tactical_server/convert_to_dict/* && coverage report --show-missing