from flask_restx import Namespace, fields


class authDto:
    api = Namespace("auth", description="使用者登入相關")

    google_args = api.model(
        "GoogleArgs",
        {
            "token": fields.String(
                required=True,
                description="Google Token",
            ),
        },
    )

    response_model = api.model(
        "RespModel",
        {
            "retMsg": fields.String(
                required=True,
                description="登入失敗",
            ),
            "retCode": fields.Integer(
                required=True,
                description="錯誤代碼",
            ),
            "retVal": fields.List(
                fields.String,
                required=True,
                description="回傳資料",
            ),
        },
    )
