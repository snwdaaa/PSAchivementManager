# 전체 게임 리스트를 가져오고, 거기에서 필요한 정보만 가져와 반환하는 스크립트
from psnawp_api import psnawp
import userInfo
import login

# 유저 인스턴스 선언
userInfoInstance = userInfo.UserInfo(login.onlineID, login.npssoCode).GetPlayerInstance()

# 전체 게임 정보가 담겨있는 딕셔너리
entireGameList = userInfoInstance.GetPlayerGames()

# 게임의 총 개수
totalTitleCount = entireGameList['totalItemCount']

# 플레이어가 소유한 게임의 정보를 가져온다
# 정보 : 게임 이름, 게임 아이콘, 플레이한 플랫폼, npCommunicationID, 전체 트로피 수, 얻은 트로피 수, 진행도(퍼센트)
# JSON Object에서 trophyTitleName, trophyTitleIconUrl, trophyTitlePlatform 가져오기
def GetOwnedGameList():
    # trophyTitleName, trophyTitleIconUrl, trophyTitlePlatform만 따로 뽑아서 새로운 딕셔너리 만들기

    # entireGameList를 바탕으로, 정리한 자료들을 담을 딕셔너리
    titleInfo = {
        'titleName' : [],
        'titleIcon' : [],
        'titlePlatform' : [],
        'npComId' : [],
        'entireTrophy' : [],
        'earnedTrophy' : [],
        'progress' : []
    }

    # 리스트 처리
    for i in range(0, totalTitleCount):
        titleName = entireGameList['trophyTitles'][i]['trophyTitleName'] # 개별 게임의 이름을 가져옴
        titleInfo['titleName'].append(titleName)

        titleIcon = entireGameList['trophyTitles'][i]['trophyTitleIconUrl'] # 개별 게임의 아이콘 URL을 가져옴
        titleInfo['titleIcon'].append(titleIcon)

        titlePlatform = entireGameList['trophyTitles'][i]['trophyTitlePlatform'] # 개별 게임의 플레이 플랫폼을 가져옴
        titleInfo['titlePlatform'].append(titlePlatform)

        npComId = entireGameList['trophyTitles'][i]['npCommunicationId'] # 개별 게임의 npCommunicationId를 가져옴
        titleInfo['npComId'].append(npComId)

        # entireTrophy와 earnedTrophy는 리스트 안에 딕셔너리{'bronze':숫자, 'silver':숫자, 'gold':숫자, 'platinum':숫자}가 또 있음
        entireTrophy = entireGameList['trophyTitles'][i]['definedTrophies'] # 개별 게임의 전체 트로피 수를 가져옴
        titleInfo['entireTrophy'].append(entireTrophy)

        earnedTrophy = entireGameList['trophyTitles'][i]['earnedTrophies'] # 개별 게임의 획득한 트로피 수를 가져옴
        titleInfo['earnedTrophy'].append(earnedTrophy)

        progress = entireGameList['trophyTitles'][i]['progress'] # 개별 게임의 트로피 진척도(퍼센트)를 가져옴
        titleInfo['progress'].append(progress)
        
    return titleInfo