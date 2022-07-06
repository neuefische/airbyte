#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class Attributes(BaseModel):
    field_type: str = Field(..., alias="field-type")
    value: List[str]


class Links1(BaseModel):
    self: str
    related: str


class Data(BaseModel):
    type: str
    id: str


class CustomField(BaseModel):
    links: Links1
    data: Data


class Links2(BaseModel):
    self: str
    related: str


class Owner(BaseModel):
    links: Links2


class Relationships(BaseModel):
    custom_field: CustomField = Field(..., alias="custom-field")
    owner: Owner


class ModelItem(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


class Model(BaseModel):
    __root__: List[ModelItem]


with open("custom_field_values.json", "w") as f:
    f.write(ModelItem.schema_json(indent=2))
