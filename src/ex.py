from psnawp_api import psnawp

# npsso code
psnawp = psnawp.PSNAWP('7aeNyvyb2TBY2XGIMSXwxdhdHYnl2ua4y7scAYH8JcgNze1urao0CHNw4C47menP')

# Make userID instance
user_onlineID = psnawp.user(online_id="kkj48188")
# 현재 모든 게임 가져오기
#print(user_onlineID.GetPlayerGames())
# 용과같이 5 PS4 버전 트로피 가져오기
#print(user_onlineID.GetAllTrophies('trophy', 'NPWR15942_00', 'all'))
# 용과같이 6 ps4 버전 클리어한 트로피 가져오기
#print(user_onlineID.GetEarnedTrophies('trophy', 'NPWR09911_00', 'all'))

# 딕셔너리 타입으로 반환함
print(type(user_onlineID.GetEarnedTrophies('trophy', 'NPWR09911_00', 'all')))