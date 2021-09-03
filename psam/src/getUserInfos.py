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

# 유저의 총 트로피 개수를 가져옴
def GetUserProfileTrophies():
    trophySummary = userInfoInstance.GetTrophyProfileSummary()

    # 유저의 전체 트로피 개수를 트로피 별로 가져온다
    trophyCount_bronze = trophySummary['earnedTrophies']['bronze']
    trophyCount_silver = trophySummary['earnedTrophies']['silver']
    trophyCount_gold = trophySummary['earnedTrophies']['gold']
    trophyCount_platinum = trophySummary['earnedTrophies']['platinum']

    # 전체 트로피 개수
    trophyCount_total = trophyCount_bronze + trophyCount_silver + trophyCount_gold + trophyCount_platinum

    # 유저 트로피 정보를 딕셔너리 형태로 내보낸다
    userTrophyCountInfo = {
        'bronze' : trophyCount_bronze,
        'silver' : trophyCount_silver,
        'gold' : trophyCount_gold,
        'platinum' : trophyCount_platinum,
        'total' : trophyCount_total
    }

    return userTrophyCountInfo

# 유저의 프로필 레벨을 가져옴 (나중에 추가)
def GetUserProfileTrophyLevel():
    trophySummary = userInfoInstance.GetTrophyProfileSummary()
    
    return trophySummary['trophyLevel']