#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class Attributes(BaseModel):
    cover_letter: Any = Field(..., alias="cover-letter")
    created_at: str = Field(..., alias="created-at")
    referring_site: Any = Field(..., alias="referring-site")
    referring_url: Any = Field(..., alias="referring-url")
    rejected_at: Any = Field(..., alias="rejected-at")
    sourced: bool
    updated_at: str = Field(..., alias="updated-at")
    row_order: int = Field(..., alias="row-order")
    changed_stage_at: str = Field(..., alias="changed-stage-at")


class Links1(BaseModel):
    self: str
    related: str


class Candidate(BaseModel):
    links: Links1


class Links2(BaseModel):
    self: str
    related: str


class Data(BaseModel):
    type: str
    id: str


class Job(BaseModel):
    links: Links2
    data: Data


class Links3(BaseModel):
    self: str
    related: str


class Data1(BaseModel):
    type: str
    id: str


class Stage(BaseModel):
    links: Links3
    data: Data1


class Links4(BaseModel):
    self: str
    related: str


class RejectReason(BaseModel):
    links: Links4
    data: Any


class Relationships(BaseModel):
    candidate: Candidate
    job: Job
    stage: Stage
    reject_reason: RejectReason = Field(..., alias="reject-reason")


class ModelItem(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


class Model(BaseModel):
    __root__: List[ModelItem]


with open("job_applications_gen.json", "w") as f:
    f.write(ModelItem.schema_json(indent=2))
