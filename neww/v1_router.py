from fastapi import APIRouter
from src.api.v1.controller import UserController
from src.api.v1.controller import FileController
from src.api.v1.controller import ClubController
from src.api.v1.controller import AttributesController
from src.api.v1.controller import EventController
from src.api.v1.controller import FeedController
from src.api.v1.controller import ExploreController
from src.api.v1.controller import ManagementController


class V1Router(APIRouter):
    def __init__(
        self,
        user_controller: UserController,
        file_controller: FileController,
        club_controller: ClubController,
        attributes_controller: AttributesController,
        event_controller: EventController,
        feed_controller: FeedController,
        explore_controller: ExploreController,
        management_controller: ManagementController,
        prefix: str = "/v1",
    ):
        super().__init__(prefix=prefix)

        self.responses = {
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "error message.",
                        }
                    }
                },
            },
            "401": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "error message.",
                        }
                    }
                },
            },
            "403": {
                "description": "Forbidden",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "error message.",
                        }
                    }
                },
            },
            "404": {
                "description": "Not Found",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "error message.",
                        }
                    }
                },
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "error message.",
                        }
                    }
                },
            },
            "422": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "error message.",
                        }
                    }
                },
            },
        }

        self.include_router(user_controller)
        self.include_router(file_controller)
        self.include_router(club_controller)
        self.include_router(attributes_controller)
        self.include_router(event_controller)
        self.include_router(feed_controller)
        self.include_router(explore_controller)
        self.include_router(management_controller)
