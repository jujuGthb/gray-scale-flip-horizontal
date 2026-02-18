from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    FirstExecutor,
    FirstExecutorResponse,
    FirstExecutorOutputs,
    OutputImage,
)


def build_response(context):
    outputImage = OutputImage(value=context.image)
    firstExecutorOutputs = FirstExecutorOutputs(outputImage=outputImage)
    firstExecutorResponse = FirstExecutorResponse(outputs= firstExecutorOutputs)
    firstExecutor = FirstExecutor(value=firstExecutorResponse)
    executor = ConfigExecutor(value=firstExecutor)
    packageConfigs = PackageConfigs(executor=executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=packageConfigs
    )

    return package.build_model(context)
