from fastapi import HTTPException
from starlette import status


class HubException(HTTPException):
    def __init__(self, status_code: int, detail: dict):
        super().__init__(status_code=status_code, detail=detail)


    @classmethod
    def internal_server_error(cls) -> "HubException":
        detail = {
            "error_en": "Critical failure",
            "error_nl": "Paniek",
        }
        return HubException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

    @classmethod
    def should_never_happen(cls) -> "HubException":
        detail = {
            "error_en": "This could should be unreachable .. you win?",
            "error_nl": "Deze code zou niet moeten kunnen runnen .. hoe heb je dat gedaan?",
        }
        return HubException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

    @classmethod
    def not_implemented(cls) -> "HubException":
        detail = {
            "error_en": "This feature is not yet implemented!",
            "error_nl": "Feature is nog niet afgewerkt!",
        }
        return HubException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=detail,
        )

    @classmethod
    def unauthorized(cls) -> "HubException":
        detail = {
            "error_en": "You are not authorized to perform this action.",
            "error_nl": "Je kan deze actie niet uitvoeren",
        }
        return HubException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    @classmethod
    def must_be_authenticated(cls) -> "HubException":
        detail = {
            "error_en": "You must be authenticated for this",
            "error_nl": "Hiervoor moet je ingelogd zijn",
        }
        return HubException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    @classmethod
    def not_found(cls):
        return HubException(
            status_code=status.HTTP_404_NOT_FOUND, detail={
                "error_en": "Not found",
                "error_nl": "Niet gevonden"
            }
        )

    @classmethod
    def resource_not_found(cls, resource: str, identifier: str) -> "HubException":
        return HubException(
            status_code=status.HTTP_404_NOT_FOUND, detail={
                "error_en": f"Resource {resource} with identifier {identifier} not found",
                "error_nl": f"Resource {resource} met idenfitier {identifier} niet gevonden"
            }
        )
