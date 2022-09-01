#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#
from abc import ABC
from datetime import datetime
from typing import Any, Iterable, Mapping, MutableMapping, Optional
from urllib.parse import parse_qs, urlparse

import pendulum
import requests
from airbyte_cdk.sources.streams.core import IncrementalMixin
from airbyte_cdk.sources.streams.http import HttpStream


# Basic full refresh stream
class TeamtailorStream(HttpStream, ABC):
    """
    This class represents a stream output by the connector.
    This is an abstract base class meant to contain all the common functionality at the API level e.g: the API base URL, pagination strategy,
    parsing responses etc..

    Each stream should extend this class (or another abstract subclass of it) to specify behavior unique to that stream.
    """

    url_base: str = "https://api.teamtailor.com/v1/"
    relations: Iterable[str] = []  # list of relations to be fetched by child classes

    def __init__(self, start_date: datetime, api_version: str, **kwargs):
        super().__init__(**kwargs)
        self.start_date = start_date
        # self.start_date = config.get("start_date") or (pendulum.now() - pendulum.duration(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.api_version = api_version

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        """
        :param response: the most recent response from the API
        :return the next page token if there is one, None otherwise
        """
        # TODO write testcase for last page
        decoded_response = response.json()
        next_page = decoded_response["links"].get("next", False)
        if next_page:
            return {"page": next_page}
        return None

    def request_params(self, next_page_token: Mapping[str, Any] = None, **kwargs) -> MutableMapping[str, Any]:
        """parse page number from next_page_token and return it as a request param"""
        relations_params = {"include": ",".join(self.relations), "page[size]": 10}
        if next_page_token:
            parse_url = urlparse(next_page_token["page"])
            query = parse_qs(parse_url.query)
            return relations_params | {"page[number]": query["page[number]"][0]}
        return relations_params

    def request_headers(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        """
        set request_headers other than authenticator
        """
        return {"X-Api-Version": self.api_version}

    # TODO implement loading schema from pydantic
    # def get_json_schema(self) -> Mapping[str, Any]:
    # return ResourceSchemaLoader(package_name_from_class(self.__class__)).get_schema(self.name)

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        """
        :return an iterable containing each record in the response
        """
        # TODO write testcase for empty data
        response_json = response.json()
        yield from response_json.get("data", [])


class IncrementalTeamtailorStream(TeamtailorStream, IncrementalMixin):
    cursor_field = "updated-at"
    cursor_filter = "filter[updated-at][from]"
    state_checkpoint_interval = 100

    def __init__(self, start_date: datetime, api_version: str, **kwargs):
        super().__init__(start_date, api_version, **kwargs)
        self._cursor_value = start_date

    @property
    def state(self) -> Mapping[str, Any]:
        if self._cursor_value:
            return {self.cursor_field: self._cursor_value.isoformat()}
        else:
            return {self.cursor_field: self.start_date.isoformat()}

    @state.setter
    def state(self, value: Mapping[str, Any]):
        if value[self.cursor_field]:
            self._cursor_value = pendulum.parse(value[self.cursor_field])
        else:
            self._cursor_value = self.start_date

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = super().request_params(stream_state=stream_state, stream_slice=stream_slice, next_page_token=next_page_token)
        params[self.cursor_filter] = (
            stream_state[self.cursor_field] if stream_state and self.cursor_field in stream_state else self.start_date.isoformat()
        )
        return params

    def read_records(self, *args, **kwargs) -> Iterable[Mapping[str, Any]]:
        for record in super().read_records(*args, **kwargs):
            latest_record_date = pendulum.parse(record["attributes"][self.cursor_field])
            self._cursor_value = max(self._cursor_value, latest_record_date)
            yield record


class JobApplications(IncrementalTeamtailorStream):
    """define how to load the data from the locations stream"""

    primary_key = "id"
    relations = ["job", "stage", "reject-reason", "candidate"]

    def path(self, **kwargs) -> str:
        """route for job applications"""
        return "job-applications"

    def request_params(self, stream_state=None, **kwargs):
        stream_state = stream_state or {}
        params = super().request_params(stream_state=stream_state, **kwargs)
        params["sort"] = "updated-at"
        return params


class Jobs(TeamtailorStream):
    """
    define how to load the data from the job stream

    This can not be incremental as filtering does not work
    """

    primary_key = "id"
    relations = []

    def path(self, **kwargs) -> str:
        """route for jobs"""
        return "jobs"

    def request_params(self, stream_state=None, **kwargs):
        stream_state = stream_state or {}
        params = super().request_params(stream_state=stream_state, **kwargs)
        params["sort"] = "updated-at"
        params["filter[status]"] = "unlisted"
        params["page[size]"] = 5
        return params


class Candidates(IncrementalTeamtailorStream):
    """define how to load the data from the candidate stream"""

    primary_key = "id"
    relations = ["job-applications", "custom-field-values"]

    def path(self, **kwargs) -> str:
        """route for candidates"""
        return "candidates"

    def request_params(self, stream_state=None, **kwargs):
        stream_state = stream_state or {}
        params = super().request_params(stream_state=stream_state, **kwargs)
        params["sort"] = "updated-at"
        return params


class CustomFieldValues(TeamtailorStream):
    """define how to load the data from the candidate stream"""

    primary_key = "id"
    relations = ["custom-field"]

    def path(self, **kwargs) -> str:
        """return path for custom field values"""
        return "custom-field-values"


class Stages(TeamtailorStream):
    """define how to load the data from the candidate stream"""

    primary_key = "id"
    relations = ["job-applications", "job", "triggers"]

    def path(self, **kwargs) -> str:
        """return path for stages"""
        return "stages"

    def request_params(self, stream_state=None, **kwargs):
        stream_state = stream_state or {}
        params = super().request_params(stream_state=stream_state, **kwargs)
        params["sort"] = "updated-at"
        return params


class Locations(TeamtailorStream):
    """define how to load the data from the locations stream"""

    primary_key = "id"

    def path(self, **kwargs) -> str:
        """route for the locations stream"""
        return "locations"
