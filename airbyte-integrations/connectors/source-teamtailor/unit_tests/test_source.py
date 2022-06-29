#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from unittest.mock import MagicMock

import pytest
from source_teamtailor.source import SourceTeamtailor


@pytest.mark.skip(reason="no way of currently testing this")
def test_check_connection(mocker):
    source = SourceTeamtailor()
    logger_mock, config_mock = MagicMock(), MagicMock()
    assert source.check_connection(logger_mock, config_mock) == (True, None)


def test_streams(mocker):
    source = SourceTeamtailor()
    config_mock = MagicMock()
    streams = source.streams(config_mock)
    expected_streams_number = 6
    assert len(streams) == expected_streams_number
