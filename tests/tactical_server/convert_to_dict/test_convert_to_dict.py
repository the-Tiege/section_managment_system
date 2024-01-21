from tactical_server.convert_to_dict.convert_to_dict import convert_to_dict
import pytest
from unittest.mock import patch, MagicMock 

TEST_DATA = [
    (
        "ID:862097,lat:52.65913,long:-8.62513",
        ({'ID': '862097', 'lat': '52.65913', 'long': '-8.62513'})
    ),
    (
        "id:862097,lat:52.65913,long:-8.62513",
        ({'id': 862097, 'lat': '52.65913', 'long': '-8.62513'})
    )
]


@pytest.mark.parametrize("message, expected_result", TEST_DATA)
def test_convert_to_dict( message, expected_result):
    result = convert_to_dict(message)

    assert result == expected_result



# coverage run --source=/home/tiege/code_portfolio/section-monitoring-system/tactical_server/convert_to_dict/ -m pytest /home/tiege/code_portfolio/section-monitoring-system/tests/tactical_server/convert_to_dict/ --ignore=/home/tiege/code_portfolio/section-monitoring-system/tests/tactical_server/convert_to_dict/* && coverage report --show-missing