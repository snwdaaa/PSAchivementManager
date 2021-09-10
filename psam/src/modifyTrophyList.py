# 전체 트로피 리스트를 가져오고, 거기에서 필요한 정보만 가져와 디셔너리 형태로 반환하는 스크립트
from psnawp_api import psnawp
import userInfo
import login

# 유저 인스턴스 선언
userInfoInstance = userInfo.UserInfo(login.onlineID, login.npssoCode).GetPlayerInstance()

# npServiceName, npCommunicationId 가져오기

allTrophyList = userInfoInstance.GetAllTrophies('trophy', 'NPWR09911_00')
earnedTrophyList = userInfoInstance.GetEarnedTrophies('trophy', 'NPWR09911_00')

totalTrophyCount = allTrophyList['totalItemCount']

def GetGameTrophyList():
    # specific menu에 넘겨줄 정리된 트로피 딕셔너리
    # 각 key에 대한 value 값은 리스트 -> 출력할 때 순서대로 출력
    resultTrophyList = {
        'isEarned' : [], # 트로피 획득 여부
        'trophyType' : [], # 트로피 등급
        'trophyName' : [], # 트로피 이름
        'trophyDetail' : [], # 트로피 설명
        'trophyIconUrl' : [], # 트로피 사진 URL
        'trophyEarnedRate' : [], # 전체 플레이어 획득 비율(%)
    }

    for i in range(0, totalTrophyCount):
        # 트로피 획득 여부
        isEarned = earnedTrophyList['trophies'][i]['earned'] # 획득 여부 boolean 값 가져옴
        resultTrophyList['isEarned'].append(isEarned)

        # 트로피 등급
        trophyType = allTrophyList['trophies'][i]['trophyType']
        resultTrophyList['trophyType'].append(trophyType)

        # 트로피 이름
        trophyName = allTrophyList['trophies'][i]['trophyName']
        resultTrophyList['trophyName'].append(trophyName)

        # 트로피 설명
        trophyDetail = allTrophyList['trophies'][i]['trophyDetail']
        resultTrophyList['trophyDetail'].append(trophyDetail)

        # 트로피 사진 URL
        trophyIconUrl = allTrophyList['trophies'][i]['trophyIconUrl']
        resultTrophyList['trophyIconUrl'].append(trophyIconUrl)

        # 전체 플레이어 획득 비율
        trophyEarnedRate = earnedTrophyList['trophies'][i]['trophyEarnedRate']
        resultTrophyList['trophyEarnedRate'].append(trophyEarnedRate)

    return resultTrophyList