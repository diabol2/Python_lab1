class ToolkitError(Exception):
    pass


class TokenizationError(ToolkitError):
    pass


class ValidationError(ToolkitError):
    pass


class CalculationError(ToolkitError):
    pass


class ConversionError(ToolkitError):
    pass