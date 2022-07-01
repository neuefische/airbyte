#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from source_teamtailor.source import TeamtailorStream
from source_teamtailor.streams import JobApplications


@pytest.fixture
def patch_base_class(mocker):
    # Mock abstract methods to enable instantiating abstract class
    mocker.patch.object(TeamtailorStream, "path", "v0/example_endpoint")
    mocker.patch.object(TeamtailorStream, "primary_key", "test_primary_key")
    mocker.patch.object(TeamtailorStream, "__abstractmethods__", set())


@pytest.fixture(name="config")
def config_fixture():
    config = {"authenticator": "authenticator", "start_date": "2022-05-01", "api_version": "20210218"}
    return config


@pytest.mark.skip(reason="no way of currently testing this")
def test_request_params(patch_base_class):
    stream = TeamtailorStream()
    # TODO: replace this with your input parameters
    inputs = {"stream_slice": None, "stream_state": None, "next_page_token": None}
    # TODO: replace this with your expected request parameters
    expected_params = {}
    assert stream.request_params(**inputs) == expected_params


@pytest.mark.skip(reason="no way of currently testing this")
def test_next_page_token(patch_base_class):
    stream = JobApplications()

    json_inputs = {
        "data": [
            {
                "id": "1234",
                "attributes": {"sourced": True},
                "relationships": {
                    "candidate": {"data": {"id": "1234", "type": "candidates"}},
                    "job": {"data": {"id": "5678", "type": "jobs"}},
                },
            }
        ]
    }

    inputs = {"response": MagicMock(json=MagicMock(return_value=json_inputs))}
    expected_token = None
    assert stream.next_page_token(**inputs) == expected_token


def test_parse_job_application_response():
    stream = JobApplications()

    json_inputs = {
        "data": [
            {
                "id": "1234",
                "attributes": {"sourced": True},
                "relationships": {
                    "candidate": {"data": {"id": "1234", "type": "candidates"}},
                    "job": {"data": {"id": "5678", "type": "jobs"}},
                },
            }
        ]
    }

    inputs = {"response": MagicMock(json=MagicMock(return_value=json_inputs))}

    expected_parsed_object = {"id": "1234", "sourced": True, "candidate_id": "1234", "job_id": "5678"}
    assert next(stream.parse_response(**inputs)) == expected_parsed_object


def test_parse_job_application_responnse_no_relation():
    """test reponse parsing when no relationship is present"""
    stream = JobApplications()

    json_inputs = {
        "data": [
            {
                "id": "1234",
                "attributes": {"sourced": True},
                "relationships": {"candidate": {}, "job": {}, "stage": {}, "reject-reason": {}},
            }
        ]
    }

    inputs = {"response": MagicMock(json=MagicMock(return_value=json_inputs))}

    expected_parsed_object = {"id": "1234", "sourced": True}
    assert next(stream.parse_response(**inputs)) == expected_parsed_object


@pytest.mark.skip(reason="no way of currently testing this")
def test_request_headers(patch_base_class):
    stream = TeamtailorStream()
    # TODO: replace this with your input parameters
    inputs = {"stream_slice": None, "stream_state": None, "next_page_token": None}
    # TODO: replace this with your expected request headers
    expected_headers = {}
    assert stream.request_headers(**inputs) == expected_headers


@pytest.mark.skip(reason="no way of currently testing this")
def test_http_method(patch_base_class):
    stream = TeamtailorStream()
    # TODO: replace this with your expected http request method
    expected_method = "GET"
    assert stream.http_method == expected_method


@pytest.mark.parametrize(
    ("http_status", "should_retry"),
    [
        (HTTPStatus.OK, False),
        (HTTPStatus.BAD_REQUEST, False),
        (HTTPStatus.TOO_MANY_REQUESTS, True),
        (HTTPStatus.INTERNAL_SERVER_ERROR, True),
    ],
)
@pytest.mark.skip(reason="no way of currently testing this")
def test_should_retry(patch_base_class, http_status, should_retry):
    response_mock = MagicMock()
    response_mock.status_code = http_status
    stream = TeamtailorStream()
    assert stream.should_retry(response_mock) == should_retry


@pytest.mark.skip(reason="no way of currently testing this")
def test_backoff_time(patch_base_class):
    response_mock = MagicMock()
    stream = TeamtailorStream()
    expected_backoff_time = None
    assert stream.backoff_time(response_mock) == expected_backoff_time
