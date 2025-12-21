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
    
    @staticmethod
    def _build_response(
        status_code: int,
        message: str,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        error_details: Optional[Union[Dict, List, str]] = None,
        success: bool = True
    ) -> Dict[str, Any]:
        """Build standardized response dictionary"""
        response = {
            'success': success,
            'status_code': status_code,
            'message': message,
        }
        
        if data is not None:
            response['data'] = data
        
        if error:
            response['error'] = error
            
        if error_details:
            response['error_details'] = error_details
            
        return response
    
    @staticmethod
    def success(
        data: Optional[Any] = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK
    ) -> Dict[str, Any]:
        """Success response"""
        return ApiResponse._build_response(
            status_code=status_code,
            message=message,
            data=data,
            success=True
        )
    
    @staticmethod
    def created(
        data: Optional[Any] = None,
        message: str = "Created successfully"
    ) -> Dict[str, Any]:
        """Created (201) response"""
        return ApiResponse._build_response(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=data,
            success=True
        )
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        error: Optional[str] = None,
        error_details: Optional[Union[Dict, List, str]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Dict[str, Any]:
        """Error response"""
        return ApiResponse._build_response(
            status_code=status_code,
            message=message,
            error=error or message,
            error_details=error_details,
            success=False
        )
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> Dict[str, Any]:
        """Not found (404) response"""
        return ApiResponse._build_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error=message,
            error_details=error_details,
            success=False
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Unauthorized access",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> Dict[str, Any]:
        """Unauthorized (401) response"""
        return ApiResponse._build_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error=message,
            error_details=error_details,
            success=False
        )
    
    @staticmethod
    def forbidden(
        message: str = "Access forbidden",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> Dict[str, Any]:
        """Forbidden (403) response"""
        return ApiResponse._build_response(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error=message,
            error_details=error_details,
            success=False
        )
    
    @staticmethod
    def validation_error(
        errors: Union[Dict, List, str],
        message: str = "Validation failed"
    ) -> Dict[str, Any]:
        """Validation error (422) response"""
        return ApiResponse._build_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error=message,
            error_details=errors,
            success=False
        )
    
    @staticmethod
    def server_error(
        message: str = "Internal server error",
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> Dict[str, Any]:
        """Server error (500) response"""
        return ApiResponse._build_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error=message,
            error_details=error_details,
            success=False
        )
    
    @staticmethod
    def custom(
        status_code: int,
        message: str,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        error_details: Optional[Union[Dict, List, str]] = None
    ) -> Dict[str, Any]:
        """Custom response"""
        success = 200 <= status_code < 300
        return ApiResponse._build_response(
            status_code=status_code,
            message=message,
            data=data,
            error=error,
            error_details=error_details,
            success=success
        )


class DRFResponse:
    """
    Django REST Framework Response Wrapper
    Converts ApiResponse to DRF Response objects
    """
    
    @staticmethod
    def send(response_data: Dict[str, Any]) -> Response:
        """Convert ApiResponse dict to DRF Response"""
        status_code = response_data.pop('status_code', status.HTTP_200_OK)
        return Response(response_data, status=status_code)
    
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
    def json(response_data: Dict[str, Any]) -> JsonResponse:
        """Convert ApiResponse dict to Django JsonResponse"""
        status_code = response_data.get('status_code', 200)
        return JsonResponse(response_data, status=status_code)
    
    @staticmethod
    def context(response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert ApiResponse to template context
        Useful for rendering in Django templates
        """
        return {
            'response': response_data,
            'success': response_data.get('success', False),
            'message': response_data.get('message', ''),
            'data': response_data.get('data'),
            'error': response_data.get('error'),
            'error_details': response_data.get('error_details'),
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
