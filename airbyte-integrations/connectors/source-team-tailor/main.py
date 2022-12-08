#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_team_tailor import SourceTeamTailor

if __name__ == "__main__":
    source = SourceTeamTailor()
    launch(source, sys.argv[1:])
