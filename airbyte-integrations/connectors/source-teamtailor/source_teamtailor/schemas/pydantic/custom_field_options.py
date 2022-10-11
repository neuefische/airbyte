#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class Attributes(BaseModel):
    value: str


class Links1(BaseModel):
    self: str
    related: str


class CustomField(BaseModel):
    links: Links1


class Relationships(BaseModel):
    custom_field: CustomField = Field(..., alias="custom-field")


class Datum(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


class Model(BaseModel):
    data: List[Datum]


with open("custom_field_options.json", "w") as f:
    f.write(Datum.schema_json(indent=2))
