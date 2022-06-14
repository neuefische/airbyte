#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from typing import Any, Iterable, List, Mapping

from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources.declarative.interpolation.interpolated_mapping import InterpolatedMapping
from airbyte_cdk.sources.declarative.interpolation.jinja import JinjaInterpolation
from airbyte_cdk.sources.declarative.stream_slicers.stream_slicer import StreamSlicer
from airbyte_cdk.sources.declarative.types import Config


class ListStreamSlicer(StreamSlicer):
    """
    Stream slicer that iterates over the values of a list
    """

    def __init__(self, slice_values: List[str], slice_definition: Mapping[str, Any], config: Config):
        self._interpolation = InterpolatedMapping(slice_definition, JinjaInterpolation())
        self._slice_values = slice_values
        self._config = config

    def stream_slices(self, sync_mode: SyncMode, stream_state: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
        return [self._interpolation.eval(self._config, slice_value=slice_value) for slice_value in self._slice_values]