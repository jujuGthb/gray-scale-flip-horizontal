
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# Inputs of the first executor


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
            return type_value

    class Config:
        title = "Image"
        
#================For second executor==========
class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"
    Optional: bool = True

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, Image):
            return "object"
        elif isinstance(actual_value, list):
            return type_value

    class Config:
        title = "Second Image"
    

class SecondExecutorInputs(Inputs):
    inputImage1: InputImage  # Reuse existing InputImage class
    inputImage2: InputImage2 # New second input


# ==================== SECOND EXECUTOR CONFIGS ====================
# Option 1: Resize (Number + String)
class ScaleValue(Config):
    name: Literal["Scale"] = "Scale"
    value: float = 0.5
    type: Literal["number"] = "number"
    field: Literal["slider"] = "slider"
    class Config: title = "Scale Factor"

class ResizeMethod(Config):
    name: Literal["Method"] = "Method"
    value: Literal["area", "linear", "cubic"] = "area"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"
    class Config: title = "Interpolation"

# Option 2: Rotate (Bool + Number)
class RotateEnable(Config):
    name: Literal["Enable"] = "Enable"
    value: bool = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config: title = "Enable Rotation"

class RotateAngle(Config):
    name: Literal["Angle"] = "Angle"
    value: int = 90
    type: Literal["number"] = "number"
    field: Literal["slider"] = "slider"
    class Config: title = "Angle Degrees"

# Dropdown Options
class ResizeMode(Config):
    name: Literal["Resize"] = "Resize"
    value: Union[ScaleValue, ResizeMethod] # 2 types: number + string
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Resize Image"
        json_schema_extra = {"target": "value"}

class RotateMode(Config):
    name: Literal["Rotate"] = "Rotate"
    value: Union[RotateEnable, RotateAngle] # 2 types: bool + number
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

class SecondExecutorConfigs(Configs):
    processingMode: ProcessingMode


# ==================== SECOND EXECUTOR OUTPUTS (2 Outputs) ====================
class OutputImage2(Output):
    name: Literal["outputImage2"] = "outputImage2"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, Image): return "object"
        elif isinstance(actual_value, list): return "list"
        return type_value
    class Config: title = "Secondary Output"

class SecondExecutorOutputs(Outputs):
    outputImage1: OutputImage  # Reuse existing
    outputImage2: OutputImage2 # New second output


# ==================== SECOND EXECUTOR WRAPPER ====================
class SecondExecutorRequest(Request):
    inputs: Optional[SecondExecutorInputs]
    configs: SecondExecutorConfigs
    class Config: json_schema_extra = {"target": "configs"}

class SecondExecutorResponse(Response):
    outputs: SecondExecutorOutputs

class SecondExecutor(Config):
    name: Literal["SecondExecutor"] = "SecondExecutor"
    value: Union[SecondExecutorRequest, SecondExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "SecondExecutor"
        json_schema_extra = {"target": {"value": 1}}

# UPDATE ConfigExecutor to include SecondExecutor
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor, SecondExecutor] # ✅ Both here
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        json_schema_extra = {"target": "value"}
        
        

    
#================For second executor==========


# ---------- configs---------------

#  Option 1   

class SimpleText(Config):
    name: Literal["Text"]= "Text"
    value:str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    
    class Config:
        title = "Text"

class SimpleNumber(Config):
    name: Literal["Number"]= "Number"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    
    class Config:
        title = "Number"

        
# Option 2

class EnableFlag(Config):
    name: Literal["Enable"] = "Enable"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"
        
class ModeSelect(Config):
    name: Literal["Mode"] = "Mode"
    value: Literal["Mode1", "Mode2", "Mode3"] = "Mode1"
    type: Literal["string"] = "string"
    field: Literal["selectBox"] = "selectBox"
    

# Dependent dropdown

class Grayscale(Config):
    name: Literal["Grayscale"] = "Grayscale"
    value: Union[SimpleText, SimpleNumber]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Convert to Grayscale"
        json_schema_extra = {
            "target": "value"
        }
class FlipHorizontal(Config):
    name: Literal["Flip Horizontal"] = "Flip Horizontal"
    value: Union[EnableFlag, ModeSelect]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Flip Horizontally"
        json_schema_extra = {
            "target": "value"
        }



class Operation(Config):
    name: Literal["Operation"] = "Operation"
    value: Union[Grayscale, FlipHorizontal]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    
    class Config:
        title = "Operation"
        json_schema_extra = {
            "target": "value"
        }

    
class FirstExecutorInputs(Inputs):
    inputImage: InputImage
class FirstExecutorConfigs(Configs):
    operation: Operation

# Outputs
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, type_value, values):
        actual_value = values.get('value')
        if isinstance(actual_value, Image):
            return "object"
        elif isinstance(actual_value, list):
            return type_value

    class Config:
        title = "Image"
        



class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }
        
class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage
    
class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs

class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    
    class Config:
        title = "FirstExecutor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }



class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor]
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