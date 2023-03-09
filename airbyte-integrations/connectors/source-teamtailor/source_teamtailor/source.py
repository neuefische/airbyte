#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


from typing import Any, List, Mapping, Tuple

import pendulum
import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http.requests_native_auth import TokenAuthenticator
from source_teamtailor.streams import (
    Candidates,
    CustomFieldOptions,
    CustomFields,
    CustomFieldValues,
    JobApplications,
    Jobs,
    Stages,
    TeamtailorStream,
)

"""
This is the source class for Teamtailor.
"""


class SourceTeamtailor(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, Any]:
        """
        check_connection is used to check if the source is able to connect to the source.

        :param config:  the user-input config object conforming to the connector's spec.yaml
        :param logger:  logger object
        :return Tuple[bool, any]: (True, None) if the input config can be used to connect to the API successfully, (False, error) otherwise.
        """
        try:
            access_token = config["access_token"]
            api_version = config["api_version"]
            headers = {"Authorization": f"Token token={access_token}", "X-Api-Version": f"{api_version}"}
            # TODO check if there is a general api to call without route
            resp = requests.get(f"{TeamtailorStream.url_base}/departments", headers=headers, data={})
            status = resp.status_code
            logger.info(f"Ping response code: {status}")
            if status == 200:
                return True, None
            error = resp.json().get("error")
            message = error.get("message") or error.get("info")
            return False, message

        except Exception as e:
            return False, e

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        authenticator = TokenAuthenticator(auth_method="Token", token=config["access_token"])
        start_date = pendulum.parse(config["start_date"])
        args = {"authenticator": authenticator, "start_date": start_date, "api_version": config["api_version"]}
        return [
            JobApplications(**args),
            Candidates(**args),
            Jobs(**args),
            Stages(**args),
            CustomFields(**args),
            CustomFieldValues(custom_field_ids=config["custom_field_ids"], **args),
            CustomFieldOptions(custom_field_ids=config["custom_field_ids"], **args),
        ]
