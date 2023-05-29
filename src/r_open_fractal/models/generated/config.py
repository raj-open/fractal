# generated by datamodel-codegen:
#   filename:  config-schema.yaml

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Extra, Field


class ConfigPeano(BaseModel):
    """
    Structure of general configuration.
    """

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    transformations: List[str] = Field(
        ..., description='Representation of transformation.'
    )


class Config(BaseModel):
    """
    Structure of general configuration.
    """

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    peano: ConfigPeano
