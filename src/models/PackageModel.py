from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)

# --- INPUTS ---
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"

    class Config:
        title = "Primary Image"

# --- CONFIGS (Bottom-Up) ---
class SimpleNumber(Config):
    name: Literal["SimpleNumber"] = "SimpleNumber"
    value: int = Field(default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Number Value"

class OptionGrayscale(Config):
    name: Literal["optionGrayscale"] = "optionGrayscale" # Optionlar camelCase
    value: SimpleNumber
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Grayscale Mode"
        json_schema_extra = {"target": "value"}

class ConfigOperation(Config):
    name: Literal["ConfigOperation"] = "ConfigOperation" # Ana config PascalCase
    value: Union[OptionGrayscale] 
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Operation Select"
        json_schema_extra = {"shortDescription": "Select processing task", "target": "value"}

# --- EXECUTOR REQUEST/RESPONSE ---
class FirstExecutorInputs(Inputs):
    inputImage: InputImage

class FirstExecutorConfigs(Configs):
    operation: ConfigOperation

class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class FirstExecutorResponse(Response):
    outputs: Outputs # Basitleştirilmiş veya özel output sınıfı

# --- TOP LEVEL ---
class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Processor"
        json_schema_extra = {"target": {"value": 0}} # Her zaman Request'i hedefle

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor] # Diğer executorları buraya ekle
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task selection"

class PackageModel(Package):
    configs: Configs
    type: Literal["component"] = "component"
    name: Literal["ImageProcessingPackage"] = "ImageProcessingPackage"