from sdks.novavision.src.helper.package import PackageHelper
from components.GrayScaleFlipHorizontal.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    FirstExecutor,
    FirstExecutorResponse,
    FirstExecutorOutputs,
    OutputImage,
    SecondExecutor,
    SecondExecutorResponse,
    SecondExecutorOutputs,
    OutputImage2
)


def build_response(context):
    if hasattr(context, "image"):

        outputImage = OutputImage(value=context.image)
        firstExecutorOutputs = FirstExecutorOutputs(outputImage=outputImage)
        firstExecutorResponse = FirstExecutorResponse(outputs=firstExecutorOutputs)
        executor_value = FirstExecutor(value=firstExecutorResponse)

    elif hasattr(context, "outputImage1"):

        outputImage1 = OutputImage(value=context.outputImage1)
        outputImage2 = OutputImage2(value=context.outputImage2)
        secondExecutorOutputs = SecondExecutorOutputs(outputImage1=outputImage1,outputImage2=outputImage2)
        secondExecutorResponse = SecondExecutorResponse(outputs=secondExecutorOutputs)
        executor_value = SecondExecutor(value=secondExecutorResponse)

    else:
        raise Exception("Unknown executor context")

    executor = ConfigExecutor(value=executor_value)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=packageConfigs
    )

    packageModel = package.build_model(context)

    return packageModel
