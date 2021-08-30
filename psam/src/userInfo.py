import psnawp_api


class UserInfo:

    def __init__(self, onlineID, npssoCode):
        self.onlineID = onlineID
        self.npssoCode = npssoCode

    # user 인스턴스를 리턴
    def GetPlayerInstance(self):
        # user를 psnawp의 user함수가 아니라 모듈 user로 인식중
        # 임시 npsso code
        psnawp = psnawp_api.psnawp.PSNAWP(self.npssoCode)
        user_onlineID = psnawp.user(online_id=self.onlineID)
        return user_onlineID

