from typing import Final


class FmuSchemaUrls:
    """These URLs can be constructed programmatically from radixconfig.yaml if need be:

        {cfg.components[].name}-{cfg.metadata.name}-{spec.environments[].name}

    As they are unlikely to change they are hardcoded here.
    """

    DEV_URL: Final[str] = "https://main-fmu-schemas-dev.radix.equinor.com"
    PROD_URL: Final[str] = "https://main-fmu-schemas-prod.radix.equinor.com"
