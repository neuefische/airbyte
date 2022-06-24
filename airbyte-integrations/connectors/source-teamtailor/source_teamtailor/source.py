#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


from airbyte_cdk.sources.abstract_source import logging
import requests
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.requests_native_auth import TokenAuthenticator
from source_teamtailor.streams import *


"""
TODO: Most comments in this class are instructive and should be deleted after the source is implemented.

This file provides a stubbed example of how to use the Airbyte CDK to develop both a source connector which supports full refresh or and an
incremental syncs from an HTTP API.

The various TODOs are both implementation hints and steps - fulfilling all the TODOs should be sufficient to implement one basic and one incremental
stream from a source. This pattern is the same one used by Airbyte internally to implement connectors.

The approach here is not authoritative, and devs are free to use their own judgement.

There are additional required TODOs in the files within the integration_tests folder and the spec.yaml file.
"""


# Source
class SourceTeamtailor(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """
        TODO: Implement a connection check to validate that the user-provided config can be used to connect to the underlying API

        See https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-stripe/source_stripe/source.py#L232
        for an example.

        :param config:  the user-input config object conforming to the connector's spec.yaml
        :param logger:  logger object
        :return Tuple[bool, any]: (True, None) if the input config can be used to connect to the API successfully, (False, error) otherwise.
        """
        try:
            access_token = config["access_token"]
            api_version = config["api_version"]
            headers = {"Authorization": f"Token token={access_token}", "X-Api-Version": f"{api_version}"}
            resp = requests.get(f"{TeamtailorStream.url_base}/departments", headers=headers, data={})
            status = resp.status_code
            logger.info(f"Ping response code: {status}")
            if status == 200:
                return True, None
            # When API requests is sent but the requested data is not available or the API call fails
            # for some reason, a JSON error is returned.
            # https://exchangeratesapi.io/documentation/#errors
            error = resp.json().get("error")
            code = error.get("code")
            message = error.get("message") or error.get("info")
            return False, message

        except Exception as e:
            return False, e

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        TODO: Replace the streams below with your own streams.

        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        # TODO remove the authenticator if not required.
        auth = TokenAuthenticator(auth_method="Token", token=config["access_token"])
        logging.info(f"Creating Teamtailor streams with config: {auth.auth_header}")
        return [Locations(authenticator=auth), JobApplications(authenticator=auth), Candidates(authenticator=auth), Custom_field_values(authenticator=auth), Stages(authenticator=auth)]
