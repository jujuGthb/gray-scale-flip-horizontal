from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)

# --- Inputs ---
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, list):
            return "list"
        return "object"

    class Config:
        title = "Primary Image"

class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Optional[Union[List[Image], Image]] = None
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, list):
            return "list"
        return "object"

    class Config:
        title = "Secondary Image"

# --- Outputs ---
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        return "list" if isinstance(actual_value, list) else "object"

    class Config:
        title = "Output Image"

class OutputImage2(Output):
    name: Literal["outputImage2"] = "outputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        return "list" if isinstance(actual_value, list) else "object"

    class Config:
        title = "Secondary Output"

# --- Parameters ---

# First Executor Parameters
class SimpleText(Config):
    name: Literal["SimpleText"] = "SimpleText"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Text"

class SimpleNumber(Config):
    name: Literal["SimpleNumber"] = "SimpleNumber"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Number"

class EnableFlag(Config):
    name: Literal["enable"] = "enable"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ModeSelect(Config):
    name: Literal["ModeSelect"] = "ModeSelect"
    value: Literal["Mode1", "Mode2", "Mode3"] = "Mode1"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"
    class Config:
        title = "Modes"

class OptionGrayscale(Config):
    name: Literal["optionGrayscale"] = "optionGrayscale"
    value: Union[SimpleText, SimpleNumber]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Convert to Grayscale"
        json_schema_extra = {"target": "value"}

class OptionFlipHorizontal(Config):
    name: Literal["optionFlipHorizontal"] = "optionFlipHorizontal"
    value: Union[EnableFlag, ModeSelect]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Flip Horizontally"
        json_schema_extra = {"target": "value"}

class ConfigOperation(Config):
    name: Literal["ConfigOperation"] = "ConfigOperation"
    value: Union[OptionGrayscale, OptionFlipHorizontal]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Operation"
        json_schema_extra = {"target": "value"}

# Second Executor Parameters
class ScaleValue(Config):
    name: Literal["ScaleValue"] = "ScaleValue"
    value: float = 0.5
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput" # Slider desteklenmiyor, textInput'a çekildi
    class Config:
        title = "Scale Factor"

class ResizeMethod(Config):
    name: Literal["ResizeMethod"] = "ResizeMethod"
    value: Literal["area", "linear", "cubic"] = "area"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"
    class Config:
        title = "Interpolation"

class RotateEnable(Config):
    name: Literal["rotateEnable"] = "rotateEnable"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable Rotation"

class RotateAngle(Config):
    name: Literal["RotateAngle"] = "RotateAngle"
    value: int = 90
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Angle Degrees"

class OptionResize(Config):
    name: Literal["optionResize"] = "optionResize"
    value: Union[ScaleValue, ResizeMethod]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Resize Image"
        json_schema_extra = {"target": "value"}

class OptionRotate(Config):
    name: Literal["optionRotate"] = "optionRotate"
    value: Union[RotateEnable, RotateAngle]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Rotate Image"
        json_schema_extra = {"target": "value"}

class ConfigProcessingMode(Config):
    name: Literal["ConfigProcessingMode"] = "ConfigProcessingMode"
    value: Union[OptionResize, OptionRotate]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Processing Mode"
        json_schema_extra = {"target": "value"}

# --- Executor Aggregations ---

class FirstExecutorInputs(Inputs):
    inputImage: InputImage

class SecondExecutorInputs(Inputs):
    inputImage1: InputImage 
    inputImage2: Optional[InputImage2]

class FirstExecutorConfigs(Configs):
    operation: ConfigOperation

class SecondExecutorConfigs(Configs):
    processingMode: ConfigProcessingMode

# --- Requests and Responses ---

class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class SecondExecutorRequest(Request):
    inputs: Optional[SecondExecutorInputs]
    configs: SecondExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage

class SecondExecutorOutputs(Outputs):
    outputImage1: OutputImage  
    outputImage2: OutputImage2 

class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs

class SecondExecutorResponse(Response):
    outputs: SecondExecutorOutputs

# --- Top Level Executors ---

class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "First Executor"
        json_schema_extra = {"target": {"value": 0}}

class SecondExecutor(Config):
    name: Literal["SecondExecutor"] = "SecondExecutor"
    value: Union[SecondExecutorRequest, SecondExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Second Executor"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor, SecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task Selection"
        json_schema_extra = {"shortDescription": "Gray Scale or Flip Horizontal processing tasks"}

# --- Package Structure ---

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayScaleFlipHorizontal"] = "GrayScaleFlipHorizontal"