from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# ==================== INPUTS ====================
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, Image):
            return "object"
        elif isinstance(actual_value, list):
            return "list"
        return type_value

    class Config:
        title = "Image"


class FirstExecutorInputs(Inputs):
    inputImage: InputImage


# ==================== CONFIG FIELDS (Leaf Nodes) ====================
# These are now DIRECT attributes of Grayscale/FlipHorizontal

# Option 1 - Grayscale params (2 different field types: string + number)
class GrayscaleText(Config):
    name: Literal["GrayscaleText"] = "GrayscaleText"
    value: str = "default_text"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    
    class Config:
        title = "Text Parameter"

class GrayscaleNumber(Config):
    name: Literal["GrayscaleNumber"] = "GrayscaleNumber"
    value: int = 50
    type: Literal["number"] = "number"
    field: Literal["slider"] = "slider"
    
    class Config:
        title = "Number Parameter"


# Option 2 - Flip params (2 different field types: bool + string)
class FlipEnable(Config):
    name: Literal["FlipEnable"] = "FlipEnable"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable Flip"
        
class FlipMode(Config):
    name: Literal["FlipMode"] = "FlipMode"
    value: Literal["Mode1", "Mode2", "Mode3"] = "Mode1"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"
    
    class Config:
        title = "Flip Mode"


# ==================== DEPENDENT DROPDOWN OPTIONS ====================
# Each option contains its fields as DIRECT attributes (not wrapped in Union)

class Grayscale(Config):
    name: Literal["Grayscale"] = "Grayscale"
    grayscaleText: GrayscaleText  # ✅ Direct attribute (field type 1: string)
    grayscaleNumber: GrayscaleNumber  # ✅ Direct attribute (field type 2: number)
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Convert to Grayscale"
        json_schema_extra = {
            "fields": ["GrayscaleText", "GrayscaleNumber"]  # ✅ Tell UI which fields to show
        }

class FlipHorizontal(Config):
    name: Literal["Flip Horizontal"] = "Flip Horizontal"
    flipEnable: FlipEnable  # ✅ Direct attribute (field type 1: bool)
    flipMode: FlipMode  # ✅ Direct attribute (field type 2: string)
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Flip Horizontally"
        json_schema_extra = {
            "fields": ["FlipEnable", "FlipMode"]  # ✅ Tell UI which fields to show
        }


# ==================== MAIN DEPENDENT DROPDOWN ====================
class Operation(Config):
    name: Literal["Operation"] = "Operation"
    value: Union[Grayscale, FlipHorizontal]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    
    class Config:
        title = "Operation"
        json_schema_extra = {
            "target": "value"  # ✅ Navigate to Grayscale or FlipHorizontal
        }


class FirstExecutorConfigs(Configs):
    operation: Operation


# ==================== OUTPUTS ====================
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, Image):
            return "object"
        elif isinstance(actual_value, list):
            return "list"
        return type_value

    class Config:
        title = "Image"

class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage


# ==================== REQUEST/RESPONSE ====================
class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }
        
class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs


# ==================== EXECUTOR WRAPPER ====================
class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: FirstExecutorRequest
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    
    class Config:
        title = "FirstExecutor"
        json_schema_extra = {
            "target": "value"
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: FirstExecutor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {   
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayScaleFlipHorizontal"] = "GrayScaleFlipHorizontal"