from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMsgbox
from typing import Collection

# 이미지 처리를 위한 모듈
from PIL import Image, ImageTk
from io import BytesIO
from urllib import request

import getUserInfos
import modifyGameList
import modifyTrophyList
import language

# Specific Menu가 열렸는지 확인하기 위한 변수
isSpecificMenuOpened = False

# region 메인 메뉴 클래스


class MainMenu:
    def __init__(self, root):
        self.root = root

        # 프로그램 기본 설정

        # 1. 언어
        # 프로그램 언어 기본 설정 -> 영어
        self.lang_setting = language.lang_en

        # 2. 게임 목록
        # 게임 목록 리스트박스에 사용되는 게임 정보가 담긴 딕셔너리
        self.ownedGameList = modifyGameList.GetOwnedGameList()

        # 기본 호출 함수
        # 1. 상단 메뉴
        self.CreateAllMenuWidgets()

        # 2. 플레이어 정보
        self.CreateAllProfileWidgets()

        # 3. 게임 목록
        self.CreateAllGameListWidgets()

        # 4. 게임 정보
        self.CreateAllGameInfoWidgets()

        # 5. 버튼
        self.CreateAllButtonWidgets()

        # 상단 메뉴
        self.root.config(menu=self.programMenu)

# region : 상단 메뉴

    # 메뉴 종류
    # self.programMenu : 메뉴 프레임
    # self.menu_program : 프로그램 메뉴
    # self.menu_language : 언어 설정 메뉴

    # 메인 메뉴에서 상단 메뉴들을 관리할 메뉴 프레임 만듦

    def CreateProgramMenuFrame(self):
        # 프로그램(다시 불러오기, 프로그램 종료), 언어 설정(English, 한국어)
        self.programMenu = Menu(self.root)

    # 상단에 프로그램 메뉴를 만듦
    def CreateProgramMenu(self):
        # 프로그램 메뉴
        self.menu_program = Menu(self.programMenu, tearoff=0)
        self.menu_program.add_command(
            label=self.lang_setting['lang_program_quit'], command=self.root.quit)
        self.programMenu.add_cascade(
            label=self.lang_setting['lang_program'], menu=self.menu_program)

    # 언어 변경 기능
    def SetLanguage(self, currentLang):
        global isSpecificMenuOpened

        # Specific Menu가 열린 상태라면 경고창을 띄운 후 함수 종료
        if(isSpecificMenuOpened == True):
            tkMsgbox.showwarning(
                self.lang_setting['lang_langSetWarn'], self.lang_setting['lang_langSetWarnDesc'])
            return

        if(currentLang == "English"):
            self.lang_setting = language.lang_en
        elif(currentLang == "Korean"):
            self.lang_setting = language.lang_ko

        self.UpdateAllWidgets()

    # 상단에 언어 설정 메뉴를 만듦
    def CreateLanguageMenu(self):
        # 언어 메뉴
        self.menu_language = Menu(self.programMenu, tearoff=0)

        # SetLanguage 함수에 인자를 전달하기 위해 람다 함수 사용
        self.menu_language.add_radiobutton(
            label="English", command=lambda: self.SetLanguage("English"))
        self.menu_language.add_radiobutton(
            label="한국어", command=lambda: self.SetLanguage("Korean"))

        # programMenu에 menu_language 메뉴 등록
        self.programMenu.add_cascade(
            label=self.lang_setting['lang_language'], menu=self.menu_language)

    # 모든 메뉴 위젯을 만드는 함수
    def CreateAllMenuWidgets(self):
        self.CreateProgramMenuFrame()  # 메뉴 프레임 만들기
        self.CreateProgramMenu()  # 프로그램 메뉴 만들기
        self.CreateLanguageMenu()  # 언어 선택 메뉴 만들기

# endregion

# region 플레이어 정보
    # 프로필 사진, 이름, 트로피 현황, 트로피 레벨 표시

    # 변수
    # self.playerInfoFrame : 플레이어 정보 표시 프레임
    # self.trophyTotalName : 현재 트로피 상태 위에 표시되는 Label
    # self.trophyLevelName : 현재 트로피 레벨 위에 표시되는 Label

    # 플레이어 정보 표시 프레임을 만듦
    def CreatePlayerInfoFrame(self):
        self.playerInfoFrame = LabelFrame(
            self.root, text=self.lang_setting['lang_profile'])
        self.playerInfoFrame.pack(side="top")

    # 프로필 사진 표시
    def ShowProfilePicture(self):
        profilePictureURL = request.urlopen(
            getUserInfos.GetUserProfileImageURL())
        raw_data = profilePictureURL.read()
        profilePictureURL.close()

        profilePictureImage = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(profilePictureImage)

        profilePictureLabel = Label(self.playerInfoFrame, image=photo)
        profilePictureLabel.image = photo
        profilePictureLabel.grid(row=0, column=1)

    # 프로필 이름 표시
    def ShowProfileName(self):
        profileName = getUserInfos.GetUserProfileName()

        profileNameLabel = Label(self.playerInfoFrame, text=profileName)
        profileNameLabel.grid(row=0, column=2)

    # 트로피 현황 표시
    def ShowProfileTrophyStatus(self):
        # 전체 트로피 수 표시
        trophyTotalName = Label(
            self.playerInfoFrame, text=self.lang_setting['lang_profile_trophyCount'])
        trophyTotalName.grid(row=1, column=2)

        userProfileTrophyInfo = getUserInfos.GetUserProfileTrophies()
        trophyTotalCount = Label(self.playerInfoFrame,
                                 text=userProfileTrophyInfo['total'])
        trophyTotalCount.grid(row=2, column=2)

        # 트로피 사진 표시
        trophyImage_bronze = PhotoImage(file="media/bronze.png")
        trophyImage_silver = PhotoImage(file="media/silver.png")
        trophyImage_gold = PhotoImage(file="media/gold.png")
        trophyImage_platinum = PhotoImage(file="media/platinum.png")

        trophyImageLabel_bronze = Label(
            self.playerInfoFrame, image=trophyImage_bronze)
        trophyImageLabel_bronze.image = trophyImage_bronze
        trophyImageLabel_bronze.grid(row=4, column=0)
        trophyImageLabel_silver = Label(
            self.playerInfoFrame, image=trophyImage_silver)
        trophyImageLabel_silver.image = trophyImage_silver
        trophyImageLabel_silver.grid(row=4, column=1)
        trophyImageLabel_gold = Label(
            self.playerInfoFrame, image=trophyImage_gold)
        trophyImageLabel_gold.image = trophyImage_gold
        trophyImageLabel_gold.grid(row=4, column=2)
        trophyImageLabel_platinum = Label(
            self.playerInfoFrame, image=trophyImage_platinum)
        trophyImageLabel_platinum.image = trophyImage_platinum
        trophyImageLabel_platinum.grid(row=4, column=3)

        # 트로피별 수 표시
        trophyCount_bronze = userProfileTrophyInfo['bronze']
        trophyCount_silver = userProfileTrophyInfo['silver']
        trophyCount_gold = userProfileTrophyInfo['gold']
        trophyCount_platinum = userProfileTrophyInfo['platinum']

        trophyCountLabel_bronze = Label(
            self.playerInfoFrame, text=trophyCount_bronze)
        trophyCountLabel_bronze.grid(row=5, column=0)
        trophyCountLabel_silver = Label(
            self.playerInfoFrame, text=trophyCount_silver)
        trophyCountLabel_silver.grid(row=5, column=1)
        trophyCountLabel_gold = Label(
            self.playerInfoFrame, text=trophyCount_gold)
        trophyCountLabel_gold.grid(row=5, column=2)
        trophyCountLabel_platinum = Label(
            self.playerInfoFrame, text=trophyCount_platinum)
        trophyCountLabel_platinum.grid(row=5, column=3)

        return trophyTotalName  # 설정 언어가 바뀔 때 업데이트 하기 위한 리턴값

    # 트로피 레벨 표시
    def ShowProfileTrophyLevel(self):
        trophyLevelName = Label(
            self.playerInfoFrame, text=self.lang_setting['lang_profile_trophyLevel'])
        trophyLevelName.grid(row=1, column=1)

        # 트로피 레벨 표시
        trophyLevel = Label(self.playerInfoFrame, text="LV " +
                            str(getUserInfos.GetUserProfileTrophyLevel()))
        trophyLevel.grid(row=2, column=1)

        return trophyLevelName  # 설정 언어가 바뀔 때 업데이트 하기 위한 리턴값

    # 프로필 초기화
    def CreateAllProfileWidgets(self):
        self.CreatePlayerInfoFrame()  # 플레이어 정보 프레임 만듦
        self.ShowProfilePicture()  # 정보 프레임 위에 플레이어 사진 표시
        self.ShowProfileName()  # 정보 프레임 위에 플레이어 이름 표시
        # 정보 프레임 위에 트로피 상태를 표시한 후 변수에 저장
        self.trophyTotalName = self.ShowProfileTrophyStatus()
        # 정보 프레임 위에 트로피 레벨을 표시한 후 변수에 저장
        self.trophyLevelName = self.ShowProfileTrophyLevel()

    # 트로피 상태 업데이트
    def UpdateTrophyStatus(self):
        self.trophyTotalName.config(
            text=self.lang_setting['lang_profile_trophyCount'])

    # 트로피 레벨 업데이트
    def UpdateTrophyLevel(self):
        self.trophyLevelName.config(
            text=self.lang_setting['lang_profile_trophyLevel'])

    # 설정 언어가 바뀔 때 트로피 상태와 트로피 레벨을 해당 언어로 업데이트
    def UpdateProfileWidgets(self):
        self.UpdateTrophyStatus()  # 트로피 상태 업데이트
        self.UpdateTrophyLevel()  # 트로피 레벨 업데이트
# endregion

# region 게임 목록
    # 게임 선택, 게임 사진, 게임 이름, 진행도(%), 트로피 현황, 상세 보기 버튼

    # 게임 목록 리스트 박스와 스크롤 바를 포함할 프레임을 만듦
    def CreateGameListFrame(self):
        self.gameSelection = Frame(self.root)
        self.gameSelection.pack(side="top")

    def CreateGameListbox(self):
        # 리스트 박스의 스크롤 바
        gameSelectionScrollBar = Scrollbar(self.gameSelection)
        gameSelectionScrollBar.pack(side="right", fill="y")

        # 게임 이름을 담을 리스트 박스
        self.gameNameList = Listbox(self.gameSelection, selectmode="single",
                                    height=5, yscrollcommand=gameSelectionScrollBar.set)

        # 리스트 박스에 게임 이름 추가
        for i in range(modifyGameList.totalTitleCount):
            self.gameNameList.insert(END, self.ownedGameList['titleName'][i])

        self.gameNameList.pack()  # 리스트 박스 표시
        self.gameNameList.selection_set(0)  # 시작할 때 첫 번째 게임 선택하게 하기

        gameSelectionScrollBar.config(command=self.gameNameList.yview)

    # 모든 게임 목록 관련 위젯 표시
    def CreateAllGameListWidgets(self):
        self.CreateGameListFrame()
        self.CreateGameListbox()
# endregion

# region 게임 정보 프레임
    # 선택된 게임의 정보를 담을 프레임 만듦
    def CreateGameInfoFrame(self):
        self.gameInfoFrame = LabelFrame(
            self.root, text=self.lang_setting['lang_game'])
        self.gameInfoFrame.pack(side="top")
# endregion

# region 게임 정보 Get 함수
    # Label에 적용할 게임 이미지를 가져오는 함수
    def GetGamePhoto(self, index):
        gameImageURL = request.urlopen(self.ownedGameList['titleIcon'][index])
        raw_data = gameImageURL.read()
        gameImageURL.close()

        gameImage = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(gameImage)

        return photo

    # Label에 적용할 게임 이름을 가져오는 함수
    def GetGameName(self, index):
        gameTitleName = self.ownedGameList['titleName'][index]

        return gameTitleName

    # Label에 적용할 게임 트로피 상태를 가져오는 함수
    def GetGameTrophyStatus(self, index):
        trophyStatus_bronze = str(self.ownedGameList['earnedTrophy'][index]['bronze']) + "/" + str(
            self.ownedGameList['entireTrophy'][index]['bronze'])
        trophyStatus_silver = str(self.ownedGameList['earnedTrophy'][index]['silver']) + "/" + str(
            self.ownedGameList['entireTrophy'][index]['silver'])
        trophyStatus_gold = str(self.ownedGameList['earnedTrophy'][index]['gold']) + "/" + str(
            self.ownedGameList['entireTrophy'][index]['gold'])
        trophyStatus_platinum = str(self.ownedGameList['earnedTrophy'][index]['platinum']) + "/" + str(
            self.ownedGameList['entireTrophy'][index]['platinum'])

        trophyStatus = "{} {} {} {}".format(
            trophyStatus_bronze, trophyStatus_silver, trophyStatus_gold, trophyStatus_platinum)

        return trophyStatus

    # Label에 적용할 게임 트로피 진행도를 가져오는 함수
    def GetGameTrophyProgress(self, index):
        titleProgress = self.ownedGameList['progress'][index]

        return titleProgress
# endregion

# region 게임 정보 초기화 함수
    def InitGameImage(self, index):
        # 선택한 게임의 사진 표시
        photo = self.GetGamePhoto(index)

        gameInfoImage = Label(self.gameInfoFrame, image=photo)
        gameInfoImage.image = photo
        gameInfoImage.pack()

        return gameInfoImage

    def InitGameName(self, index):
        # 선택한 게임의 이름 표시
        gameTitleName = self.GetGameName(index)

        gameInfoName = Label(self.gameInfoFrame, text=gameTitleName)
        gameInfoName.pack()

        return gameInfoName

    def InitGameTrophyStatus(self, index):
        # 선택한 게임의 트로피 현황 표시 (획득/전체)
        trophyStatus = self.GetGameTrophyStatus(index)

        gameInfoTrophy = Label(self.gameInfoFrame, text=trophyStatus)
        gameInfoTrophy.pack()

        return gameInfoTrophy

    def InitGameTrophyProgress(self, index):
        # 선택한 게임의 진행도 표시
        titleProgress = self.GetGameTrophyProgress(index)

        gameInfoProgress = Label(
            self.gameInfoFrame, text=self.lang_setting['lang_progress'] + " " + str(titleProgress) + "%")
        gameInfoProgress.pack()

        return gameInfoProgress
# endregion

# region 게임 정보 위젯 생성
    def CreateAllGameInfoWidgets(self):
        # 게임 정보를 표시할 프레임을 만듦
        self.CreateGameInfoFrame()

        # 각 위젯들을 생성한 후 멤버 변수에 대입
        self.currentIndex = self.gameNameList.curselection()[0]
        self.g_gameInfoImage = self.InitGameImage(self.currentIndex)
        self.g_gameInfoName = self.InitGameName(self.currentIndex)
        self.g_gameInfoTrophy = self.InitGameTrophyStatus(self.currentIndex)
        self.g_gameInfoProgress = self.InitGameTrophyProgress(
            self.currentIndex)
# endregion

# region 게임 정보 업데이트 함수
    # 게임 선택할 때 실행하는 업데이트 함수들

    # 게임 이미지 업데이트
    def UpdateGameImage(self, a_gameInfoImage, index):
        photo = self.GetGamePhoto(index)

        a_gameInfoImage.image = photo
        a_gameInfoImage.config(image=photo)

    # 게임 이름 업데이트
    def UpdateGameName(self, a_gameInfoName, index):
        gameTitleName = self.GetGameName(index)

        a_gameInfoName.config(text=gameTitleName)

    # 게임 트로피 상태 업데이트
    def UpdateGameTrophyStatus(self, a_gameInfoTrophy, index):
        trophyStatus = self.GetGameTrophyStatus(index)

        a_gameInfoTrophy.config(text=trophyStatus)

    # 게임 트로피 진행도 업데이트
    def UpdateGameTrophyProgress(self, a_gameInfoProgress, index):
        titleProgress = self.GetGameTrophyProgress(index)

        a_gameInfoProgress.config(
            text=self.lang_setting['lang_progress'] + " " + str(titleProgress) + "%")

    # 게임 정보 프레임 안에 있는 모든 위젯을 선택한 게임으로 업데이트한다.
    def UpdateGameInfos(self):
        # 리스트 박스의 curselection -> 튜플
        # 튜플의 맨 첫 번째 원소를 가져옴 (현재 선택한 것)
        self.currentIndex = self.gameNameList.curselection()[0]

        self.UpdateGameImage(self.g_gameInfoImage, self.currentIndex)
        self.UpdateGameName(self.g_gameInfoName, self.currentIndex)
        self.UpdateGameTrophyStatus(self.g_gameInfoTrophy, self.currentIndex)
        self.UpdateGameTrophyProgress(
            self.g_gameInfoProgress, self.currentIndex)
# endregion

# region Specific Menu 관련 함수
    # specificMenu 스크립트에 넘겨줄 정보를 딕셔너리 형태로 정리하는 함수
    def GetSelectedGameInfoDict(self):
        # 게임 이름, 사진, 트로피 현황, 진행도, 선택 언어 정보를 정리 후 넘겨준다.
        selectedGameInfo = {
            'titleName': self.GetGameName(self.currentIndex),
            # PhotoImage 자체를 가져오는 것에 주의
            'titleIcon': self.GetGamePhoto(self.currentIndex),
            'titleTrophyStatus': self.GetGameTrophyStatus(self.currentIndex),
            # 퍼센티지 숫자만 가져오는 것에 주의
            'titleTrophyProgress': self.GetGameTrophyProgress(self.currentIndex),
            'selectedLanguage': self.lang_setting,
            'npComId' : self.ownedGameList['npComId'][self.currentIndex],
            'npSerName' : self.ownedGameList['npSerName'][self.currentIndex]
        }

        return selectedGameInfo

    # 게임 세부 정보 창을 띄우는 함수
    def ShowGameSpecificInfoWindow(self):
        global isSpecificMenuOpened

        gameInfoDict = self.GetSelectedGameInfoDict()
        SpecificMenu.gameInfoDict = gameInfoDict  # Specific Menu로 게임 정보 전달

        # Specific Menu의 상태(열림, 닫힘)을 저장하는 변수
        isSpecificMenuOpened = True

        # root를 Toplevel로 하는 SpecificMenu를 띄움
        self.specificMenu = SpecificMenu(self.root)

    # Specific Menu를 닫을 때, 창을 닫기 전까지 보았던 게임을 gameNameList에서 선택하게 함
    # 선택하지 않으면 언어 설정을 바꿀 때 gameNameList의 요소들 중 아무 것도 선택되어 있지 않아 오류가 발생
    def SelectElementOnList(self):
        self.gameNameList.select_set(self.currentIndex)

# endregion

# region 버튼
    # 선택한 게임의 상세 보기 버튼을 표시

    def CreateGameInfoSpecificButton(self):
        self.gameInfoSpecific = Button(
            self.gameInfoFrame, text=self.lang_setting['lang_specific'], command=self.ShowGameSpecificInfoWindow)
        self.gameInfoSpecific.pack()

    # 게임 선택 버튼을 표시
    def CreateGameSelectButton(self):
        self.gameSelectionBtn = Button(
            self.gameSelection, text=self.lang_setting['lang_gameSelect'], command=self.UpdateGameInfos)  # 업데이트
        self.gameSelectionBtn.pack()

    # 모든 버튼 표시
    def CreateAllButtonWidgets(self):
        self.CreateGameInfoSpecificButton()
        self.CreateGameSelectButton()
# endregion

# region 모든 위젯 업데이트
    # 언어 변경할 때 모든 위젯을 새로 불러옴
    def UpdateAllWidgets(self):
        self.UpdateGameInfos()
        self.gameInfoSpecific.config(
            text=self.lang_setting['lang_specific'])  # 세부 정보 버튼
        self.gameSelectionBtn.config(
            text=self.lang_setting['lang_gameSelect'])  # 게임 선택 버튼
        self.playerInfoFrame.config(
            text=self.lang_setting['lang_profile'])  # 플레이어 정보 프레임
        self.gameInfoFrame.config(
            text=self.lang_setting['lang_game'])  # 게임 정보 프레임
        # entryconfig 함수 : 메뉴 안의 옵션을 config
        # 상단 메뉴 업데이트.
        self.menu_program.entryconfig(
            1, label=self.lang_setting['lang_program_quit'])
        self.programMenu.entryconfig(
            1, label=self.lang_setting['lang_program'])  # 상단 메뉴 업데이트
        self.programMenu.entryconfig(
            2, label=self.lang_setting['lang_language'])  # 상단 메뉴 업데이트
        # 트로피 관련 업데이트
        self.UpdateTrophyStatus()
        self.UpdateTrophyLevel()
# endregion

# endregion - 메인 메뉴 클래스

# region 특정 게임 트로피 상세 정보 메뉴 클래스
class SpecificMenu:
    # main menu에서 선택한 게임의 정보와 언어 설정을 가져올 딕셔너리
    gameInfoDict = {}

    def __init__(self, root):  # root : 창의 root, gameInfo : 선택한 게임의 상세정보 및 언어정보
        self.root = root  # Toplevel이 될 root
        self.specificWindow = self.CreateSpecificMenu(self.root)  # Specific Menu

        # 언어 설정 가져오기
        self.lang_setting = self.gameInfoDict['selectedLanguage']

        # 기본 호출 함수
        # 1. 게임 정보
        self.CreateAllGameInfoWidgets()

        # 2. 정렬 콤보박스
        self.CreateSortingCombobox()

        # 3. 트로피 정보
        self.CreateAllTrophyWidgets()

        self.specificWindow.protocol(
            "WM_DELETE_WINDOW", self.OnSpecificMenuClose)  # 창이 닫힐 때 호출

    # Specific Menu를 root를 Toplevel로 가지도록 한 후, Menu를 리턴한다.
    def CreateSpecificMenu(self, root):
        specificWindow = Toplevel(root)

        specificWindow.title("PS Trophy Manager")
        specificWindow.geometry("600x750")
        specificWindow.resizable(True, True)

        return specificWindow

    # Specific Menu가 떠있는 동안 언어 변경을 막기 위한 함수
    # Specific Menu가 종료될 때, isSpecificMenuOpened를 False로 바꾼후 창을 없앤다
    def OnSpecificMenuClose(self):
        global isSpecificMenuOpened

        isSpecificMenuOpened = False
        self.specificWindow.destroy()  # 창 종료
        MainMenu.SelectElementOnList(mainMenu)

    # npServiceName, npCommunicationId를 modifyTrophyList.py로 전달한다.
    # self.gameInfoDict['npComId'] , self.gameInfoDict['npSerName']

# region 게임 정보 프레임
    def CreateGameInfoFrame(self):
        self.gameInfoFrame = LabelFrame(
            self.specificWindow, text=self.lang_setting['lang_game'])
        self.gameInfoFrame.pack(side='top', padx=10, pady=10)
# endregion

# region 게임 정보
    def InitGameImage(self):
        photo = self.gameInfoDict['titleIcon']

        gameInfoImage = Label(self.gameInfoFrame, image=photo)
        gameInfoImage.image = photo
        gameInfoImage.grid(row=1, column=0)

    def InitGameName(self):
        titleName = self.gameInfoDict['titleName']

        gameInfoName = Label(self.gameInfoFrame, text=titleName)
        gameInfoName.grid(row=0, column=1)

    def InitGameTrophyStatus(self):
        trophyStatus = self.gameInfoDict['titleTrophyStatus']

        gameTrophyStatus = Label(self.gameInfoFrame, text=trophyStatus)
        gameTrophyStatus.grid(row=1, column=1)

    def InitGameTrophyProgress(self):
        # 진행도 숫자만 가져옴
        trophyProgress = self.gameInfoDict['titleTrophyProgress']

        gameTrophyProgress = Label(
            self.gameInfoFrame, text=self.lang_setting['lang_progress'] + " " + str(trophyProgress) + "%")
        gameTrophyProgress.grid(row=2, column=1)
# endregion

# region 게임 정보 위젯 생성
    def CreateAllGameInfoWidgets(self):
        self.CreateGameInfoFrame()  # 프레임
        self.InitGameImage()  # 게임 사진
        self.InitGameName()  # 게임 이름
        self.InitGameTrophyStatus()  # 게임 트로피 상태
        self.InitGameTrophyProgress()  # 게임 트로피 진행도
# endregion

# region 트로피 정렬 콤보박스
    # 트로피 정렬을 위한 콤보박스
    def CreateSortingCombobox(self):
        # 정렬 기준
        # self.sortTypeList = ['earnedDate', 'earned', 'earnedRate', 'trophyType'] # 얻은 날짜, 획득/미획득, 전체 플레이어 달성률, 트로피 등급
        self.sortTypeList = [self.lang_setting['lang_earnedDate'], self.lang_setting['lang_earned'],
                             self.lang_setting['lang_earnedRate'], self.lang_setting['lang_trophyType']]

        # 정렬 과정에서 combobox의 값을 사용해야 하므로 self로 선언
        self.sortTypeCombobox = ttk.Combobox(
            self.specificWindow, height=3, values=self.sortTypeList, state="readonly")
        self.sortTypeCombobox.current(0)  # default값 설정
        self.sortTypeCombobox.pack(side="right", padx=10)
# endregion

# region 트로피 요소 처리
    # 게임의 트로피 정보를 딕셔너리로 가져옴
    def GetGameTrophyDict(self):
        return modifyTrophyList.GetGameTrophyList()

    # 하나의 트로피 클래스마다 하나의 트로피 정보를 넘겨주기 위해
    # 게임의 전체 트로피의 정보가 담겨있는 딕셔너리를 이용해
    # 새로운 딕셔너리를 만든다
    def ModifyTrophyDict(self, index):
        trophyDict = self.GetGameTrophyDict()

        trophyDict_individual = {
            'isEarned': 0,
            'trophyType': 0,
            'trophyName': 0,
            'trophyDetail': 0,
            'trophyIconUrl': 0,
            'trophyEarnedRate': 0,
        }

        trophyDict_individual['isEarned'] = trophyDict['isEarned'][index]
        trophyDict_individual['trophyType'] = trophyDict['trophyType'][index]
        trophyDict_individual['trophyName'] = trophyDict['trophyName'][index]
        trophyDict_individual['trophyDetail'] = trophyDict['trophyDetail'][index]
        trophyDict_individual['trophyIconUrl'] = trophyDict['trophyIconUrl'][index]
        trophyDict_individual['trophyEarnedRate'] = trophyDict['trophyEarnedRate'][index]

        return trophyDict_individual

    # 트로피 인스턴스를 생성
    def CreateTrophyInstance(self):
        # 전체 트로피 갯수
        self.trophyCount = modifyTrophyList.totalTrophyCount

        # 트로피 인스턴스를 담을 리스트
        self.trophyInstances = []

        # 해당 게임의 트로피 갯수만큼 인스턴스 생성 후 trophyInstance에 저장
        for i in range(0, self.trophyCount):
            trophyInstance = Trophy(self.ModifyTrophyDict(i))
            self.trophyInstances.append(trophyInstance)
# endregion

# region 전체 트로피 정보 프레임
    def CreateTrophyInfoFrame(self):
        self.trophyInfoFrame = LabelFrame(
            self.specificWindow, text=self.lang_setting['lang_specific'])
        self.trophyInfoFrame.pack(expand=True)
# endregion

# region 개별 트로피 정보 프레임 (반복문에서 호출)
    def CreateIndividualTrophyInfoFrame(self):
        indFrame = Frame(self.trophyInfoFrame, bd=1)
        indFrame.pack(expand=True)

        return indFrame
# endregion

# region 개별 트로피 정보 (반복문에서 호출)
    # 트로피 이미지 표시
    def InitTrophyImage(self, parentFrame, imageUrl):
        trophyImageURL = request.urlopen(imageUrl)
        raw_data = trophyImageURL.read()
        trophyImageURL.close()

        trophyImage = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(trophyImage)

        trophyInfoImage = Label(parentFrame, image=photo)
        trophyInfoImage.image = photo
        trophyInfoImage.grid(row=1, column=1)

    # 트로피 이름 표시
    def InitTrophyName(self, parentFrame, name):
        trophyInfoName = Label(parentFrame, text=name)
        trophyInfoName.grid(row=0, column=0)

    # 트로피 설명 표시
    def InitTrophyDetail(self, parentFrame, detail):
        trophyInfoDetail = Label(parentFrame, text=detail)
        trophyInfoDetail.grid(row=0, column=1)

    # 전체 플레이어 달성률 표시
    def InitTrophyEarnedRate(self, parentFrame, earnedRate):
        trophyInfoEarnedRate = Label(parentFrame, text=earnedRate)
        trophyInfoEarnedRate.grid(row=0, column=2)
# endregion

# region 개별 트로피 위젯 생성
    # 개별 트로피 정보를 담을 프레임들의 리스트를 리턴
    def CreateIndividualTrophyInfoFrameList(self):
        # 개별 트로피 정보를 담을 프레임들의 리스트
        indFrameList = []

        # 개별 트로피 프레임을 트로피 갯수만큼 만들어
        # 리스트에 저장한다
        for i in range(0, self.trophyCount):
            indFrameList.append(self.CreateIndividualTrophyInfoFrame())

        return indFrameList

    # 개별 트로피의 사진을 프레임에 pack
    def CreateIndividualTrophyImage(self):
        indFrameList = self.CreateIndividualTrophyInfoFrameList()

        # 각 프레임에 트로피 사진을 표시
        for i in range(0, self.trophyCount):
            trophyImageUrl = self.trophyInstances[i].GetTrophyIconUrl()
            self.InitTrophyImage(indFrameList[i], trophyImageUrl)

    # 개별 트로피의 이름을 프레임에 pack
    def CreateIndividualTrophyName(self):
        indFrameList = self.CreateIndividualTrophyInfoFrameList()

        # 각 프레임에 트로피 이름을 표시
        for i in range(0, self.trophyCount):
            trophyName = self.trophyInstances[i].GetTrophyName()
            self.InitTrophyName(indFrameList[i], trophyName)

    # 개별 트로피의 설명을 프레임에 pack
    def CreateIndividualTrophyDetail(self):
        indFrameList = self.CreateIndividualTrophyInfoFrameList()

        # 각 프레임에 트로피 설명을 표시
        for i in range(0, self.trophyCount):
            trophyDetail = self.trophyInstances[i].GetTrophyDetail()
            self.InitTrophyDetail(indFrameList[i], trophyDetail)

    # 개별 트로피의 획득 비율을 프레임에 pack
    def CreateIndividualTrophyEarnedRate(self):
        indFrameList = self.CreateIndividualTrophyInfoFrameList()

        # 각 프레임에 트로피 획득 비율을 표시
        for i in range(0, self.trophyCount):
            trophyEarnedRate = self.trophyInstances[i].GetTrophyEarnedRate()
            self.InitTrophyDetail(indFrameList[i], trophyEarnedRate)

    # 모든 개별 트로피 관련 위젯을 생성
    def CreateAllIndividualTrophyInfoWidget(self):
        self.CreateIndividualTrophyInfoFrameList()
        self.CreateIndividualTrophyImage()
        self.CreateIndividualTrophyName()
        self.CreateIndividualTrophyDetail()
        self.CreateIndividualTrophyEarnedRate()
# endregion

# region 트로피 위젯(트로피 프레임, 개별 트로피, 스크롤 바) 생성
    def CreateAllTrophyWidgets(self):
        self.CreateTrophyInstance()
        self.CreateTrophyInfoFrame()
        self.CreateAllIndividualTrophyInfoWidget()
# endregion


# endregion

# region 트로피 클래스
# Specific Menu의 트로피 목록에서 사용될 트로피 클래스
class Trophy:
    def __init__(self, trophyDict):
        # trophyDict : 트로피 정보가 담긴 딕셔너리
        self.trophyDict = trophyDict

# region Getting 함수
    # 해당 트로피의 획득 여부를 boolean으로 리턴
    def GetIsEarned(self):
        return self.trophyDict['isEarned']

    # 해당 트로피의 Type을 문자열로 리턴
    def GetTrophyType(self):
        return self.trophyDict['trophyType']

    # 해당 트로피의 이름을 문자열로 리턴
    def GetTrophyName(self):
        return self.trophyDict['trophyName']

    # 해당 트로피의 설명을 문자열로 리턴
    def GetTrophyDetail(self):
        return self.trophyDict['trophyDetail']

    # 해당 트로피의 사진 URL을 문자열로 리턴
    def GetTrophyIconUrl(self):
        return self.trophyDict['trophyIconUrl']

    # 해당 트로피의 전체 플레이어 획득 비율을 실수 형태로 리턴
    def GetTrophyEarnedRate(self):
        return self.trophyDict['trophyEarnedRate']
# endregion

# endregion


# region 프로그램 창 기본 설정
root = Tk()

# 기본 창 크기 설정
# 프로그램 창에 표시되는 이름
root.title("PS Trophy Manager")
# 창 크기
root.geometry("600x750")
# 창 크기 조절 가능
root.resizable(False, False)
# endregion

# Main Menu 객체
mainMenu = MainMenu(root)
root.mainloop()
