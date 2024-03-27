from basic import GoogleService


class GoogleDrive(GoogleService):
    """Google Drive Service"""

    def __init__(self):
        super().__init__()
        self.drive = self.gc.drive

    def create_folder(self, folder_name: str):
        """Create a folder in Google Drive， 且資料夾在 Test Center 資料夾下"""
        # 在檔案夾 id 1LtCULaErjvBh6422YUDAV60uGNDtit0U 底下建一個檔案夾，使用 folder metadata
        folder = self.drive.create_folder(
            folder_name, "13q7wU1Uu592nxBm63J2OgNfurLmXaD2m"
        )
        return "success"

    def list_folder(self):
        """List all folders in Google Drive"""
        folders = self.drive.list()
        for folder in folders:
            print(folder)
        return "success"

    def get_folder_metadata(self, folder_id: str):
        """Get folder metadata"""
        folder = self.drive.folder_metadata()
        print(folder)
        return "success"


GoogleDrive().create_folder("123465")
