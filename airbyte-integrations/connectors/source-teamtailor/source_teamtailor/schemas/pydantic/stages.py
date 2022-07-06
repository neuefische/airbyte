#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class Attributes(BaseModel):
    created_at: str = Field(..., alias="created-at")
    updated_at: str = Field(..., alias="updated-at")
    name: str
    stage_type: str = Field(..., alias="stage-type")
    row_order: int = Field(..., alias="row-order")
    active_job_applications_count: int = Field(..., alias="active-job-applications-count")
    rejected_job_applications_count: int = Field(..., alias="rejected-job-applications-count")


class Links1(BaseModel):
    self: str
    related: str


class Datum(BaseModel):
    type: str
    id: str


class JobApplications(BaseModel):
    links: Links1
    data: List[Datum]


class Links2(BaseModel):
    self: str
    related: str


class Triggers(BaseModel):
    links: Links2
    data: List


class Links3(BaseModel):
    self: str
    related: str


class Data(BaseModel):
    type: str
    id: str


class Job(BaseModel):
    links: Links3
    data: Data


class Relationships(BaseModel):
    job_applications: JobApplications = Field(..., alias="job-applications")
    triggers: Triggers
    job: Job


class ModelItem(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


class Model(BaseModel):
    __root__: List[ModelItem]


with open("stages.json", "w") as f:
    f.write(ModelItem.schema_json(indent=2))
