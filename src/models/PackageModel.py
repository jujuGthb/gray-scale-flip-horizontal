from pydantic import validator
from typing import List, Optional, Union, Literal

from sdks.novavision.src.base.model import (
    Package, Image,
    Inputs, Outputs, Configs,
    Response, Request,
    Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def detect_type(cls, v, values):
        val = values.get("value")
        if isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"
    optional: bool = True

    @validator("type", pre=True, always=True)
    def detect_type(cls, v, values):
        val = values.get("value")
        if isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Second Image"



class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def detect_type(cls, v, values):
        val = values.get("value")
        if isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class OutputImage2(OutputImage):
    name: Literal["outputImage2"] = "outputImage2"

    class Config:
        title = "Secondary Output"




class SimpleText(Config):
    name: Literal["Text"] = "Text"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Text"


class SimpleNumber(Config):
    name: Literal["Number"] = "Number"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Number"


class EnableFlag(Config):
    name: Literal["Enable"] = "Enable"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class ModeSelect(Config):
    name: Literal["Mode"] = "Mode"
    value: Literal["Mode1", "Mode2", "Mode3"] = "Mode1"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"

    class Config:
        title = "Mode"




class Grayscale(Config):
    name: Literal["Grayscale"] = "Grayscale"
    value: Union[SimpleText, SimpleNumber]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Convert to Grayscale"
        json_schema_extra = {"target": "value"}


class FlipHorizontal(Config):
    name: Literal["FlipHorizontal"] = "Flip Horizontal"
    value: Union[EnableFlag, ModeSelect]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Flip Horizontally"
        json_schema_extra = {"target": "value"}


class Operation(Config):
    name: Literal["Operation"] = "Operation"
    value: Union[Grayscale, FlipHorizontal]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Operation"
        json_schema_extra = {"target": "value"}




class ScaleValue(Config):
    name: Literal["Scale"] = "Scale"
    value: float = 0.5
    type: Literal["number"] = "number"
    field: Literal["slider"] = "slider"

    class Config:
        title = "Scale Factor"


class ResizeMethod(Config):
    name: Literal["Method"] = "Method"
    value: Literal["area", "linear", "cubic"] = "area"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"

    class Config:
        title = "Interpolation"


class RotateEnable(Config):
    name: Literal["Enable"] = "Enable"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable Rotation"


class RotateAngle(Config):
    name: Literal["Angle"] = "Angle"
    value: int = 90
    type: Literal["number"] = "number"
    field: Literal["slider"] = "slider"

    class Config:
        title = "Angle Degrees"


class ResizeMode(Config):
    name: Literal["Resize"] = "Resize"
    value: Union[ScaleValue, ResizeMethod]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Resize Image"
        json_schema_extra = {"target": "value"}


class RotateMode(Config):
    name: Literal["Rotate"] = "Rotate"
    value: Union[RotateEnable, RotateAngle]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Rotate Image"
        json_schema_extra = {"target": "value"}


class ProcessingMode(Config):
    name: Literal["ProcessingMode"] = "ProcessingMode"
    value: Union[ResizeMode, RotateMode]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Processing Mode"
        json_schema_extra = {"target": "value"}



class FirstExecutorInputs(Inputs):
    inputImage: InputImage


class SecondExecutorInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage2


class FirstExecutorConfigs(Configs):
    operation: Operation


class SecondExecutorConfigs(Configs):
    processingMode: ProcessingMode


class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage


class SecondExecutorOutputs(Outputs):
    outputImage1: OutputImage
    outputImage2: OutputImage2



class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs


class SecondExecutorRequest(Request):
    inputs: Optional[SecondExecutorInputs]
    configs: SecondExecutorConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class SecondExecutorResponse(Response):
    outputs: SecondExecutorOutputs



class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "FirstExecutor"
        json_schema_extra = {"target": {"value": 0}}


class SecondExecutor(Config):
    name: Literal["SecondExecutor"] = "SecondExecutor"
    value: Union[SecondExecutorRequest, SecondExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "SecondExecutor"


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor, SecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "shortDescription": "gray scale flip horizontal"
        }



class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["GrayScaleFlipHorizontal"] = "GrayScaleFlipHorizontal"
    configs: PackageConfigs
    type: Literal["component"] = "component"