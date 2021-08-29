from psnawp_api import psnawp
import userInfo
import login

# 유저 인스턴스 선언
userInfoInstance = userInfo.UserInfo(login.onlineID, login.npssoCode).GetPlayerInstance()

userProfile = userInfoInstance.profile()

#print(userProfile)

# 유저의 프로필 사진의 URL을 가져옴
def GetUserProfileImageURL():
    profileImageURL = userProfile['personalDetail']['profilePictures'][1]['url'] # size 'm'의 url을 가져옴

    return profileImageURL

# 유저의 psn 이름을 가져옴
def GetUserProfileName():
    firstName = userProfile['personalDetail']['firstName']
    lastName = userProfile['personalDetail']['lastName']
    fullName = firstName + lastName

    return fullName

# 유저의 총 프로필 개수를 가져옴
def GetUserProfileTrophies():
    pass

# 유저의 프로필 레벨을 가져옴 (나중에 추가)
def GetUserProfileTrophyLevel():
    pass