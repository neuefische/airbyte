#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class Attributes(BaseModel):
    api_name: str = Field(..., alias="api-name")
    name: str
    field_type: str = Field(..., alias="field-type")
    owner_type: str = Field(..., alias="owner-type")
    is_hidden: bool = Field(..., alias="is-hidden")
    is_private: bool = Field(..., alias="is-private")
    is_searchable: bool = Field(..., alias="is-searchable")
    is_featured: bool = Field(..., alias="is-featured")
    is_external: bool = Field(..., alias="is-external")
    is_required: bool = Field(..., alias="is-required")
    created_at: str = Field(..., alias="created-at")
    updated_at: str = Field(..., alias="updated-at")


class Links1(BaseModel):
    self: str
    related: str


class CustomFieldValues(BaseModel):
    links: Links1


class Links2(BaseModel):
    self: str
    related: str


class CustomFieldOptions(BaseModel):
    links: Links2


class Relationships(BaseModel):
    custom_field_values: CustomFieldValues = Field(..., alias="custom-field-values")
    custom_field_options: Optional[CustomFieldOptions] = Field(None, alias="custom-field-options")


class Datum(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


class Model(BaseModel):
    data: List[Datum]


with open("custom_fields.json", "w") as f:
    f.write(Datum.schema_json(indent=2))
