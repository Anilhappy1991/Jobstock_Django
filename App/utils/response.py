"""
Common Response Utility Classes
Provides standardized response formats for both REST API and Django templates
"""
from typing import Any, Optional, Dict, List, Union
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


class ApiResponse:
    """
    Standardized API Response Class
    
    Usage:
        # Success response
        return ApiResponse.success(data={'user': user_data}, message="User created successfully")
        
        # Error response
        return ApiResponse.error(message="Invalid data", errors={'email': ['Email already exists']})
        
        # Custom response
        return ApiResponse.custom(status_code=201, message="Created", data=data)
    """
    
    def __init__(self, success: bool, message: str, data: Optional[Any] = None, 
                 error: Optional[str] = None, error_details: Optional[Union[Dict, List, str]] = None,
                 status_code: int = 200):
        """Initialize ApiResponse object"""
        self.success = success
        self.message = message
        self.data = data
        self.error = error
        self.error_details = error_details
        self.status_code = status_code
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        response = {
            'success': self.success,
            'status_code': self.status_code,
            'message': self.message,
        }
        
        if self.data is not None:
            response['data'] = self.data
        
        if self.error:
            response['error'] = self.error
            
        if self.error_details:
            response['error_details'] = self.error_details
            
        return response
    
    @staticmethod
    def success(
        data: Optional[Any] = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK
    ) -> 'ApiResponse':
        """Success response"""
        return ApiResponse(
            success=True,
            message=message,
            data=data,
            status_code=status_code
        )
    
    @staticmethod
    def created(
        data: Optional[Any] = None,
        message: str = "Created successfully"
    ) -> 'ApiResponse':
        """Created (201) response"""
        return ApiResponse(
            success=True,
            message=message,
            data=data,
            status_code=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        error: Optional[str] = None,
        error_details: Optional[Union[Dict, List, str]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> 'ApiResponse':
        """Error response"""
        return ApiResponse(
            success=False,
            message=message,
            error=error or message,
            error_details=error_details,
            status_code=status_code
        )
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> 'ApiResponse':
        """Not found (404) response"""
        return ApiResponse(
            success=False,
            message=message,
            error=message,
            error_details=error_details,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Unauthorized access",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> 'ApiResponse':
        """Unauthorized (401) response"""
        return ApiResponse(
            success=False,
            message=message,
            error=message,
            error_details=error_details,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(
        message: str = "Access forbidden",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> 'ApiResponse':
        """Forbidden (403) response"""
        return ApiResponse(
            success=False,
            message=message,
            error=message,
            error_details=error_details,
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def validation_error(
        errors: Union[Dict, List, str],
        message: str = "Validation failed"
    ) -> 'ApiResponse':
        """Validation error (422) response"""
        return ApiResponse(
            success=False,
            message=message,
            error=message,
            error_details=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    @staticmethod
    def server_error(
        message: str = "Internal server error",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> 'ApiResponse':
        """Server error (500) response"""
        return ApiResponse(
            success=False,
            message=message,
            error=message,
            error_details=error_details,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @staticmethod
    def custom(
        status_code: int,
        message: str,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> 'ApiResponse':
        """Custom response"""
        success = 200 <= status_code < 300
        return ApiResponse(
            success=success,
            message=message,
            data=data,
            error=error,
            error_details=error_details,
            status_code=status_code
        )


class DRFResponse:
    """
    Django REST Framework Response Wrapper
    Converts ApiResponse to DRF Response objects
    """
    
    @staticmethod
    def send(api_response: ApiResponse) -> Response:
        """Convert ApiResponse to DRF Response"""
        return Response(api_response.to_dict(), status=api_response.status_code)
    
    @staticmethod
    def success(data: Optional[Any] = None, message: str = "Success") -> Response:
        """Success DRF response"""
        return DRFResponse.send(ApiResponse.success(data=data, message=message))
    
    @staticmethod
    def created(data: Optional[Any] = None, message: str = "Created successfully") -> Response:
        """Created DRF response"""
        return DRFResponse.send(ApiResponse.created(data=data, message=message))
    
    @staticmethod
    def error(message: str, error_details: Optional[Union[Dict, List, str]] = None, 
              status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
        """Error DRF response"""
        return DRFResponse.send(ApiResponse.error(
            message=message, 
            error_details=error_details, 
            status_code=status_code
        ))
    
    @staticmethod
    def not_found(message: str = "Resource not found") -> Response:
        """Not found DRF response"""
        return DRFResponse.send(ApiResponse.not_found(message=message))
    
    @staticmethod
    def validation_error(errors: Union[Dict, List, str], message: str = "Validation failed") -> Response:
        """Validation error DRF response"""
        return DRFResponse.send(ApiResponse.validation_error(errors=errors, message=message))


class DjangoResponse:
    """
    Django Template Response Wrapper
    Converts ApiResponse to Django JsonResponse or context dict
    """
    
    @staticmethod
    def json(api_response: ApiResponse) -> JsonResponse:
        """Convert ApiResponse to Django JsonResponse"""
        return JsonResponse(api_response.to_dict(), status=api_response.status_code)
    
    @staticmethod
    def context(api_response: ApiResponse) -> Dict[str, Any]:
        """
        Convert ApiResponse to template context
        Useful for rendering in Django templates
        """
        return {
            'response': api_response.to_dict(),
            'success': api_response.success,
            'message': api_response.message,
            'data': api_response.data,
            'error': api_response.error,
            'error_details': api_response.error_details,
        }


# Convenience functions for quick access
def success_response(data=None, message="Success"):
    """Quick success response"""
    return ApiResponse.success(data=data, message=message)


def error_response(message="Error", error_details=None, status_code=400):
    """Quick error response"""
    return ApiResponse.error(
        message=message, 
        error_details=error_details, 
        status_code=status_code
    )


def validation_response(errors, message="Validation failed"):
    """Quick validation error response"""
    return ApiResponse.validation_error(errors=errors, message=message)
