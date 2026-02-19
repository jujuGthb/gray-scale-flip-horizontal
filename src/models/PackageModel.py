
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# Inputs of the first executor


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"
        
class FirstExecutorInputs(Inputs):
    inputImage: InputImage

    

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


class FlipHorizontal(Config):
    name: Literal["Flip Horizontal"] = "Flip Horizontal"
    value: Union[EnableFlag, ModeSelect]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Flip Horizontally"



class Operation(Config):
    name: Literal["Operation"] = "Operation"
    value: Union[Grayscale, FlipHorizontal]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    
class FirstExecutorConfigs(Configs):
    operation: Operation

# Outputs
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"
        
class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage



class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }
        
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
    name: Literal["Package"] = "Package"
