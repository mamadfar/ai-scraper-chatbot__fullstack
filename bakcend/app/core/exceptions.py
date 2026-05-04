
"""
Global error classes
"""

from typing import Any # For Any type, like "unknown" in TS

# In Ts we'd do:
# export class AppError extends Error {
# Constructor(public statusCode: number, message: string) { super(message) }
# }

class AppException(Exception):
    """ Base exception for all application errors """

    def __init__(self, status_code: int, message: str, details: Any = None) -> None:
        # super().__init__() is the same as super() in TS
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.details = details

class NotFoundException(AppException):
    """ Raised when a resource is not found - maps to HTTP 404 """

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(status_code=404, message=message)

class ValidationException(AppException):
    """ Raised when input validation fails - maps to HTTP 422 """

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(status_code=422, message=message, details=details)

class ServiceException(AppException):
    """ Raised when an external service (LLM, DB, etc.) fails - maps to HTTP 503 """

    def __init__(self, message: str = "External service unavailable") -> None:
        super().__init__(status_code=503, message=message)

class UnauthorizedException(AppException):
    """ Raised when authentication fails - maps to HTTP 401 """

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(status_code=401, message=message)