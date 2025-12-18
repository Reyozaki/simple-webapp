from fastapi import HTTPException, status


class NotAuthorizedException(HTTPException):
    def __init__(self, detail: str = "Not Authorized"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW_Authenticate": "Insufficient Authority"},
        )


class AuthenticationException(HTTPException):
    def __init__(self, detail: str = "Verification failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOTFOUND,
        )
