from fastapi import status


class ApplicationException(Exception):
    """Exceção base da aplicação"""
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """Exceção para erros de validação"""
    
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message, code, status_code=status.HTTP_400_BAD_REQUEST)


class NotFoundException(ApplicationException):
    """Exceção quando recurso não é encontrado"""
    
    def __init__(self, message: str, code: str = "NOT_FOUND"):
        super().__init__(message, code, status_code=status.HTTP_404_NOT_FOUND)


class ConflictException(ApplicationException):
    """Exceção para conflito de dados"""
    
    def __init__(self, message: str, code: str = "CONFLICT"):
        super().__init__(message, code, status_code=status.HTTP_409_CONFLICT)


class UnauthorizedException(ApplicationException):
    """Exceção para autenticação não autorizada"""
    
    def __init__(self, message: str = "Não autorizado", code: str = "UNAUTHORIZED"):
        super().__init__(message, code, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(ApplicationException):
    """Exceção para acesso proibido"""
    
    def __init__(self, message: str = "Acesso proibido", code: str = "FORBIDDEN"):
        super().__init__(message, code, status_code=status.HTTP_403_FORBIDDEN)