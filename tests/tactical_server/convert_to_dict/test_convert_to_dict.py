from tactical_server.convert_to_dict.convert_to_dict import convert_to_dict
import pytest
from unittest.mock import patch, MagicMock 

TEST_DATA = [
    (
        "ID:862097,lat:52.65913,long:-8.62513",
        ({'ID': '862097', 'lat': '52.65913', 'long': '-8.62513' , 'number':1}, "Some Value")
    ),
    (
        "id:862097,lat:52.65913,long:-8.62513",
        ({'id': 862097, 'lat': '52.65913', 'long': '-8.62513', 'number':1}, "Some Value")
    )
]
@pytest.fixture
def setup():
    x = 1
    return x


@pytest.mark.parametrize("message, expected_result", TEST_DATA)
@patch("tactical_server.convert_to_dict.convert_to_dict.number_yoke")
def test_convert_to_dict(mock_number_yoke, message, expected_result, setup):
    mock_number_yoke.return_value = 1
    test_mock = MagicMock(return_value="Some Value")
    result = convert_to_dict(message, test_mock)

    assert result == expected_result



# coverage run --source=/home/tiege/code_portfolio/section-monitoring-system/tactical_server/convert_to_dict/ -m pytest /home/tiege/code_portfolio/section-monitoring-system/tests/tactical_server/convert_to_dict/ --ignore=/home/tiege/code_portfolio/section-monitoring-system/tests/tactical_server/convert_to_dict/* && coverage report --show-missing