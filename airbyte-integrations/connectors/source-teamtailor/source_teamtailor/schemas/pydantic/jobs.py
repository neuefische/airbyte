#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Links(BaseModel):
    careersite_job_url: str = Field(..., alias="careersite-job-url")
    careersite_job_internal_url: str = Field(..., alias="careersite-job-internal-url")
    careersite_job_apply_url: str = Field(..., alias="careersite-job-apply-url")
    careersite_job_apply_iframe_url: str = Field(..., alias="careersite-job-apply-iframe-url")
    self: str


class PictureItem(BaseModel):
    original: str
    standard: str
    thumb: str


class Attributes(BaseModel):
    apply_button_text: str = Field(..., alias="apply-button-text")
    body: str
    end_date: Any = Field(..., alias="end-date")
    human_status: str = Field(..., alias="human-status")
    internal: bool
    language_code: str = Field(..., alias="language-code")
    picture: Optional[PictureItem]
    pinned: bool
    start_date: Any = Field(..., alias="start-date")
    status: str
    tags: List[str]
    title: str
    pitch: str
    external_application_url: str = Field(..., alias="external-application-url")
    name_requirement: str = Field(..., alias="name-requirement")
    resume_requirement: str = Field(..., alias="resume-requirement")
    cover_letter_requirement: str = Field(..., alias="cover-letter-requirement")
    phone_requirement: str = Field(..., alias="phone-requirement")
    created_at: str = Field(..., alias="created-at")
    updated_at: str = Field(..., alias="updated-at")
    sharing_image_layout: str = Field(..., alias="sharing-image-layout")
    mailbox: str
    remote_status: str = Field(..., alias="remote-status")
    employment_type: str = Field(..., alias="employment-type")
    employment_level: str = Field(..., alias="employment-level")
    salary_time_unit: str = Field(..., alias="salary-time-unit")
    min_salary: Any = Field(..., alias="min-salary")
    max_salary: Any = Field(..., alias="max-salary")
    currency: str
    recruiter_email: str = Field(..., alias="recruiter-email")


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


class Datum(BaseModel):
    type: str
    id: str


class Role(BaseModel):
    links: Links3
    data: Optional[Datum]


class Links4(BaseModel):
    self: str
    related: str


class Location(BaseModel):
    links: Links4


class Links5(BaseModel):
    self: str
    related: str


class Datum1(BaseModel):
    type: str
    id: str


class Locations(BaseModel):
    links: Links5
    data: List[Datum1]


class Links6(BaseModel):
    self: str
    related: str


class Regions(BaseModel):
    links: Links6


class Links7(BaseModel):
    self: str
    related: str


class User(BaseModel):
    links: Links7


class Links8(BaseModel):
    self: str
    related: str


class Questions(BaseModel):
    links: Links8


class Links9(BaseModel):
    self: str
    related: str


class Datum2(BaseModel):
    type: str
    id: str


class Candidates(BaseModel):
    links: Links9
    data: List[Datum2]


class Links10(BaseModel):
    self: str
    related: str


class Datum3(BaseModel):
    type: str
    id: str


class Stages(BaseModel):
    links: Links10
    data: List[Datum3]


class Links11(BaseModel):
    self: str
    related: str


class Colleagues(BaseModel):
    links: Links11


class Links12(BaseModel):
    self: str
    related: str


class TeamMemberships(BaseModel):
    links: Links12


class Links13(BaseModel):
    self: str
    related: str


class PickedQuestions(BaseModel):
    links: Links13


class Links14(BaseModel):
    self: str
    related: str


class Requisition(BaseModel):
    links: Links14


class Links15(BaseModel):
    self: str
    related: str


class CustomFields(BaseModel):
    links: Links15


class Links16(BaseModel):
    self: str
    related: str


class CustomFieldValues(BaseModel):
    links: Links16


class Relationships(BaseModel):
    activities: Activities
    department: Department
    role: Role
    location: Location
    locations: Locations
    regions: Regions
    user: User
    questions: Questions
    candidates: Candidates
    stages: Stages
    colleagues: Colleagues
    team_memberships: TeamMemberships = Field(..., alias="team-memberships")
    picked_questions: PickedQuestions = Field(..., alias="picked-questions")
    requisition: Requisition
    custom_fields: CustomFields = Field(..., alias="custom-fields")
    custom_field_values: CustomFieldValues = Field(..., alias="custom-field-values")


class ModelItem(BaseModel):
    id: str
    type: str
    links: Links
    attributes: Attributes
    relationships: Relationships


class Model(BaseModel):
    __root__: List[ModelItem]


with open("jobs.json", "w") as f:
    f.write(ModelItem.schema_json(indent=2))
