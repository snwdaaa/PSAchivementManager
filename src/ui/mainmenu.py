from tkinter import *

root = Tk()

# 프로그램 창에 표시되는 이름
root.title("PS Trophy Manager")
# 기본 창 크기 설정
root.geometry("1200x800")
# 창 크기 조절 가능
root.resizable(True, True)

# 상단 메뉴
# 프로그램(다시 불러오기, 프로그램 종료), 언어 설정(English, 한국어)

# 플레이어 정보 표시 프레임
# 프로필 사진, 이름, 프로필 레벨 표시
playerInfoFrame = LabelFrame(root, text="플레이어 정보")
playerInfoFrame.pack(side="top")

# 프로필 사진을 가져오는 함수로부터 사진을 받아옴

# 플레이어 이름을 가져오는 함수로부터 사진을 받아옴

# 플레이어 프로필 레벨을 가져오는 함수로부터 사진을 받아옴 (나중에 추가)

# 게임 목록 프레임
# 게임 사진, 게임 이름, 진행도(%), 트로피 현황, 상세 보기 버튼

root.mainloop()