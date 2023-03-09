#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class Attributes(BaseModel):
    connected: bool
    created_at: str = Field(..., alias="created-at")
    email: str
    facebook_id: Any = Field(..., alias="facebook-id")
    first_name: str = Field(..., alias="first-name")
    internal: bool
    last_name: str = Field(..., alias="last-name")
    linkedin_uid: Any = Field(..., alias="linkedin-uid")
    linkedin_url: Any = Field(..., alias="linkedin-url")
    original_resume: Any = Field(..., alias="original-resume")
    phone: Optional[str]
    picture: Any
    pitch: Any
    referring_site: Any = Field(..., alias="referring-site")
    referring_url: Any = Field(..., alias="referring-url")
    referred: bool
    resume: Any
    sourced: bool
    unsubscribed: bool
    updated_at: str = Field(..., alias="updated-at")
    restricted_at: Any = Field(..., alias="restricted-at")
    facebook_profile: Any = Field(..., alias="facebook-profile")
    linkedin_profile: Any = Field(..., alias="linkedin-profile")
    tags: List[str]


class Links1(BaseModel):
    self: str
    related: str


class Activities(BaseModel):
    links: Links1


class Links2(BaseModel):
    self: str
    related: str


class Department(BaseModel):
    links: Links2


class Links3(BaseModel):
    self: str
    related: str


class Role(BaseModel):
    links: Links3


class Links4(BaseModel):
    self: str
    related: str


class Regions(BaseModel):
    links: Links4


class Links5(BaseModel):
    self: str
    related: str


class Datum(BaseModel):
    type: str
    id: str


class JobApplications(BaseModel):
    links: Links5
    data: List[Datum]


class Links6(BaseModel):
    self: str
    related: str


class Questions(BaseModel):
    links: Links6


class Links7(BaseModel):
    self: str
    related: str


class Answers(BaseModel):
    links: Links7


class Links8(BaseModel):
    self: str
    related: str


class Locations(BaseModel):
    links: Links8


class Links9(BaseModel):
    self: str
    related: str


class Uploads(BaseModel):
    links: Links9


class Links10(BaseModel):
    self: str
    related: str


class Datum1(BaseModel):
    type: str
    id: str


class CustomFieldValues(BaseModel):
    links: Links10
    data: List[Datum1]


class Links11(BaseModel):
    self: str
    related: str


class PartnerResults(BaseModel):
    links: Links11


class Relationships(BaseModel):
    activities: Activities
    department: Department
    role: Role
    regions: Regions
    job_applications: JobApplications = Field(..., alias="job-applications")
    questions: Questions
    answers: Answers
    locations: Locations
    uploads: Uploads
    custom_field_values: CustomFieldValues = Field(..., alias="custom-field-values")
    partner_results: PartnerResults = Field(..., alias="partner-results")


class ModelItem(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


with open("candidates.json", "w") as f:
    f.write(ModelItem.schema_json(indent=2))
