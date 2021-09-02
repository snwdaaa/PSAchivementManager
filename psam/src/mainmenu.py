from tkinter import *
import tkinter.ttk as ttk

# 이미지 처리를 위한 모듈
from PIL import Image, ImageTk
from io import BytesIO
from urllib import request

import getUserInfos
import modifyGameList
import language

# region 프로그램 창 기본 설정
root = Tk()

# 프로그램 창에 표시되는 이름
root.title("PS Trophy Manager")
# 기본 창 크기 설정
root.geometry("600x650")
# 창 크기 조절 가능
root.resizable(False, False)
# endregion

# region : 상단 메뉴
# 프로그램(다시 불러오기, 프로그램 종료), 언어 설정(English, 한국어)
programMenu = Menu(root)

# 프로그램 언어 기본 설정 -> 영어
lang_setting = language.lang_en

# 프로그램 메뉴
menu_program = Menu(programMenu, tearoff=0)
menu_program.add_command(label=lang_setting['lang_program_quit'], command=root.quit)
programMenu.add_cascade(label=lang_setting['lang_program'], menu=menu_program)

# 언어 메뉴
menu_language = Menu(programMenu, tearoff=0)

# 언어 변경
def SetLanguage(currentLang):
    # global -> 함수 밖에 있는 변수를 그대로 함수 안에서 사용할 때 사용
    global lang_setting

    if(currentLang == "English"):
        lang_setting = language.lang_en
    elif(currentLang == "Korean"):
        lang_setting = language.lang_ko

    UpdateAllWidgets()

# 언어 메뉴
# SetLanguage 함수에 인자를 전달하기 위해 람다 함수 사용
menu_language.add_radiobutton(label="English", command=lambda: SetLanguage("English"))
menu_language.add_radiobutton(label="한국어", command=lambda: SetLanguage("Korean"))

# programMenu에 menu_language 메뉴 등록
programMenu.add_cascade(label=lang_setting['lang_language'], menu=menu_language)
# endregion


# region 플레이어 정보
# 플레이어 정보 표시 프레임
# 프로필 사진, 이름, 트로피 현황, 트로피 레벨 표시
playerInfoFrame = LabelFrame(root, text=lang_setting['lang_profile'])
playerInfoFrame.pack(side="top")

# 프로필 사진
def ShowProfilePicture():
    profilePictureURL = request.urlopen(getUserInfos.GetUserProfileImageURL())
    raw_data = profilePictureURL.read()
    profilePictureURL.close()

    profilePictureImage = Image.open(BytesIO(raw_data))
    photo = ImageTk.PhotoImage(profilePictureImage)

    profilePictureLabel = Label(playerInfoFrame, image=photo)
    profilePictureLabel.image = photo
    profilePictureLabel.pack()

# 프로필 이름
def ShowProfileName():
    profileName = getUserInfos.GetUserProfileName()

    profileNameLabel = Label(playerInfoFrame, text=profileName)
    profileNameLabel.pack()

# 트로피 현황

# 트로피 레벨 (나중에 추가)

# 프로필 초기화
def InitProfile():
    ShowProfilePicture()
    ShowProfileName()
    # 트로피 현황
    # 트로피 레벨

InitProfile()
# endregion

# region 게임 목록
ownedGameList = modifyGameList.GetOwnedGameList()

# 게임 목록 프레임
# 게임 선택, 게임 사진, 게임 이름, 진행도(%), 트로피 현황, 상세 보기 버튼
gameSelection = Frame(root)
gameSelection.pack(side="top")

# 리스트 박스의 스크롤 바
gameSelectionScrollBar = Scrollbar(gameSelection)
gameSelectionScrollBar.pack(side="right", fill="y")

# 게임 이름을 담을 리스트 박스
gameNameList = Listbox(gameSelection, selectmode="single", height=5, yscrollcommand=gameSelectionScrollBar.set)

# 리스트 박스에 게임 이름 추가
for i in range(modifyGameList.totalTitleCount):
    gameNameList.insert(END, ownedGameList['titleName'][i])

gameNameList.pack()
gameNameList.selection_set(0)  # 시작할 때 첫 번째 게임 선택하게 하기

gameSelectionScrollBar.config(command=gameNameList.yview)
# 게임 정보 프레임
gameInfoFrame = LabelFrame(root, text=lang_setting['lang_game'])
gameInfoFrame.pack(side="top")
# endregion

# region 게임 목록 초기화 함수
def InitGameImage(index):
    # 선택한 게임의 사진 표시
    gameImageURL = request.urlopen(ownedGameList['titleIcon'][index])
    raw_data = gameImageURL.read()
    gameImageURL.close()

    gameImage = Image.open(BytesIO(raw_data))
    photo = ImageTk.PhotoImage(gameImage)

    gameInfoImage = Label(gameInfoFrame, image=photo)
    gameInfoImage.image = photo
    gameInfoImage.pack()
    #gameInfoImage.grid(row=0, column=0)

    return gameInfoImage


def InitGameName(index):
    # 선택한 게임의 이름 표시
    gameTitleName = ownedGameList['titleName'][index]

    gameInfoName = Label(gameInfoFrame, text=gameTitleName)
    gameInfoName.pack()
    #gameInfoName.grid(row=1, column=1)

    return gameInfoName


def InitGameTrophyStatus(index):
    # 선택한 게임의 트로피 현황 표시 (획득/전체)
    trophyStatus_bronze = str(ownedGameList['earnedTrophy'][index]['bronze']) + "/" + str(ownedGameList['entireTrophy'][index]['bronze'])
    trophyStatus_silver = str(ownedGameList['earnedTrophy'][index]['silver']) + "/" + str(ownedGameList['entireTrophy'][index]['silver'])
    trophyStatus_gold = str(ownedGameList['earnedTrophy'][index]['gold']) + "/" + str(ownedGameList['entireTrophy'][index]['gold'])
    trophyStatus_platinum = str(ownedGameList['earnedTrophy'][index]['platinum']) + "/" + str(ownedGameList['entireTrophy'][index]['platinum'])

    trophyStatus = "{} {} {} {}".format(trophyStatus_bronze, trophyStatus_silver, trophyStatus_gold, trophyStatus_platinum)

    gameInfoTrophy = Label(gameInfoFrame, text=trophyStatus)
    gameInfoTrophy.pack()
    #gameInfoTrophy.grid(row=1, column=0)

    return gameInfoTrophy


def InitGameTrophyProgress(index):
    # 선택한 게임의 진행도 표시
    titleProgress = ownedGameList['progress'][index]

    gameInfoProgress = Label(gameInfoFrame, text=lang_setting['lang_progress'] + " " + str(titleProgress) + "%")
    gameInfoProgress.pack()

    #gameInfoProgress.grid(row=2, column=0)

    return gameInfoProgress
# endregion

# 각 위젯들을 생성한 후 전역 변수에 대입
currentIndex = gameNameList.curselection()[0]
g_gameInfoImage = InitGameImage(currentIndex)
g_gameInfoName = InitGameName(currentIndex)
g_gameInfoTrophy = InitGameTrophyStatus(currentIndex)
g_gameInfoProgress = InitGameTrophyProgress(currentIndex)

# region 게임 목록 업데이트 함수
# 게임 선택할 때 실행하는 업데이트 함수들

# 게임 이미지 업데이트
def UpdateGameImage(a_gameInfoImage, index):
    gameImageURL = request.urlopen(ownedGameList['titleIcon'][index])
    raw_data = gameImageURL.read()
    gameImageURL.close()

    gameImage = Image.open(BytesIO(raw_data))
    photo = ImageTk.PhotoImage(gameImage)

    a_gameInfoImage.image = photo
    a_gameInfoImage.config(image=photo)

# 게임 이름 업데이트


def UpdateGameName(a_gameInfoName, index):
    gameTitleName = ownedGameList['titleName'][index]

    a_gameInfoName.config(text=gameTitleName)

# 게임 트로피 상태 업데이트


def UpdateGameTrophyStatus(a_gameInfoTrophy, index):
    trophyStatus_bronze = str(ownedGameList['earnedTrophy'][index]['bronze']) + "/" + str(
        ownedGameList['entireTrophy'][index]['bronze'])
    trophyStatus_silver = str(ownedGameList['earnedTrophy'][index]['silver']) + "/" + str(
        ownedGameList['entireTrophy'][index]['silver'])
    trophyStatus_gold = str(ownedGameList['earnedTrophy'][index]['gold']) + "/" + str(
        ownedGameList['entireTrophy'][index]['gold'])
    trophyStatus_platinum = str(ownedGameList['earnedTrophy'][index]['platinum']) + "/" + str(
        ownedGameList['entireTrophy'][index]['platinum'])

    trophyStatus = "{} {} {} {}".format(
        trophyStatus_bronze, trophyStatus_silver, trophyStatus_gold, trophyStatus_platinum)

    a_gameInfoTrophy.config(text=trophyStatus)

# 게임 트로피 진행도 업데이트
def UpdateGameTrophyProgress(a_gameInfoProgress, index):
    titleProgress = ownedGameList['progress'][index]

    a_gameInfoProgress.config(text=lang_setting['lang_progress'] + " " + str(titleProgress) + "%")

# 게임 정보 프레임 안에 있는 모든 위젯을 선택한 게임으로 업데이트한다.
def UpdateGameInfos():
    # 리스트 박스의 curselection -> 튜플
    # 튜플의 맨 첫 번째 원소를 가져옴 (현재 선택한 것)
    currentIndex = gameNameList.curselection()[0]

    UpdateGameImage(g_gameInfoImage, currentIndex)
    UpdateGameName(g_gameInfoName, currentIndex)
    UpdateGameTrophyStatus(g_gameInfoTrophy, currentIndex)
    UpdateGameTrophyProgress(g_gameInfoProgress, currentIndex)
# endregion

def ShowGameSpecificInfo():
    pass


# region 버튼
# 선택한 게임의 상세 보기 버튼 표시
gameInfoSpecific = Button(gameInfoFrame, text=lang_setting['lang_specific'], command=ShowGameSpecificInfo)
gameInfoSpecific.pack()
#gameInfoSpecific.grid(row=3, column=0)

# 게임 선택 버튼 --------------------
gameSelectionBtn = Button(gameSelection, text=lang_setting['lang_gameSelect'], command=UpdateGameInfos)  # 업데이트
gameSelectionBtn.pack()
# endregion

# 언어 변경할 때 모든 위젯을 새로 불러옴
def UpdateAllWidgets():
    UpdateGameInfos()
    gameInfoSpecific.config(text=lang_setting['lang_specific']) # 세부 정보 버튼
    gameSelectionBtn.config(text=lang_setting['lang_gameSelect']) # 게임 선택 버튼
    playerInfoFrame.config(text=lang_setting['lang_profile']) # 플레이어 정보 프레임
    gameInfoFrame.config(text=lang_setting['lang_game']) # 게임 정보 프레임
    # entryconfig 함수 : 메뉴 안의 옵션을 config
    menu_program.entryconfig(1, label=lang_setting['lang_program_quit']) # 상단 메뉴 업데이트.
    programMenu.entryconfig(1, label=lang_setting['lang_program']) # 상단 메뉴 업데이트
    programMenu.entryconfig(2, label=lang_setting['lang_language']) # 상단 메뉴 업데이트


root.config(menu=programMenu)
root.mainloop()
