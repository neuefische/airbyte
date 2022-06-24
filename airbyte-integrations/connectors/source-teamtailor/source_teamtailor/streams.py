#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#
from abc import ABC
from typing import Any, Iterable, Mapping, MutableMapping, Optional
from urllib.parse import parse_qs, urlparse

import requests
from airbyte_cdk.sources.streams.http import HttpStream


# Basic full refresh stream
class TeamtailorStream(HttpStream, ABC):
    """
    This class represents a stream output by the connector.
    This is an abstract base class meant to contain all the common functionality at the API level e.g: the API base URL, pagination strategy,
    parsing responses etc..

    Each stream should extend this class (or another abstract subclass of it) to specify behavior unique to that stream.
    """

    url_base = "https://api.teamtailor.com/v1/"
    relations = []  # list of relations to be fetched by child classes

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        """
        :param response: the most recent response from the API
        :return the next page token if there is one, None otherwise
        """
        decoded_response = response.json()
        next_page = decoded_response["links"].get("next", False)
        if next_page:
            return {"page": next_page}
        return None

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        """parse page number from next_page_token and return it as a request param"""
        relations_params = {"include": ",".join(self.relations)}
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
        return {"X-Api-Version": "20210218"}

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        """
        :return an iterable containing each record in the response
        """
        response_json = response.json()
        attributes = [
            {"id": item["id"]}
            | {
                item["relationships"][relation]["data"]["type"] + "_id": item["relationships"][relation]["data"]["id"]
                for relation in self.relations
                if item["relationships"][relation]["data"]
            }
            | item["attributes"]
            for item in response_json["data"]
        ]
        yield from attributes


class Locations(TeamtailorStream):
    """define how to load the data from the locations stream"""

    primary_key = "id"

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        """route for the locations stream"""
        return "locations"


class JobApplications(TeamtailorStream):
    """define how to load the data from the locations stream"""

    primary_key = "id"
    relations = ["candidate", "job", "stage", "reject-reason"]

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        """route for job applications"""
        return "job-applications"


class Companies(TeamtailorStream):
    """route for companies"""

    primary_key = "id"
    relations = ["manager"]

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        """ """
        return "companies"


class Candidates(TeamtailorStream):
    """define how to load the data from the candidate stream"""

    primary_key = "id"
    relations = [
        "activities",
        "department",
        "role",
        "job-applications",
        "questions",
        "answers",
        "locations",
        "regions",
        "uploads",
        "custom-field-values",
        "partner-results",
    ]

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        """ """
        return "candidates"


class CustomFieldValues(TeamtailorStream):
    """define how to load the data from the candidate stream"""

    primary_key = "id"
    relations = ["custom_field", "owner"]

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        """return path for custom field values"""
        return "custom-field-values"


class Stages(TeamtailorStream):
    """define how to load the data from the candidate stream"""

    primary_key = "id"
    relations = ["job-applications", "job", "triggers"]

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        """return path for stages"""
        return "stages"
