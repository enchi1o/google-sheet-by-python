class RespModel:
    def __init__(
        self,
        retMsg: str = "",
        retVal: list = [],
        retCode: int = 200,
        errCode: str = None,
        updateTime: str = None,
    ):
        self.retMsg = retMsg
        self.retVal = retVal
        self.retCode = retCode

        if errCode is not None:
            self.errCode = errCode
        if updateTime is not None:
            self.updateTime = updateTime

    def json(self):
        return self.__dict__

    def result(self):
        return self.__dict__, self.retCode
