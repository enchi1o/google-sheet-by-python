import pygsheets
import os


class GoogleService:
    """Google Auth"""

    def __init__(self):
        self.gc = pygsheets.authorize(
            service_file=os.path.join(
                os.path.dirname(__file__), "../../testcasecenter-5f9540f31782.json"
            )
        )
