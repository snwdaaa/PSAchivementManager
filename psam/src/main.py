from tkinter import *

# 이미지 처리를 위한 모듈
from PIL import Image, ImageTk
from io import BytesIO
from urllib import request

import getUserInfos
import modifyGameList
import language

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
        #gameInfoImage.grid(row=0, column=0)

        return gameInfoImage

    def InitGameName(self, index):
        # 선택한 게임의 이름 표시
        gameTitleName = self.GetGameName(index)

        gameInfoName = Label(self.gameInfoFrame, text=gameTitleName)
        gameInfoName.pack()
        #gameInfoName.grid(row=1, column=1)

        return gameInfoName

    def InitGameTrophyStatus(self, index):
        # 선택한 게임의 트로피 현황 표시 (획득/전체)
        trophyStatus = self.GetGameTrophyStatus(index)

        gameInfoTrophy = Label(self.gameInfoFrame, text=trophyStatus)
        gameInfoTrophy.pack()
        #gameInfoTrophy.grid(row=1, column=0)

        return gameInfoTrophy

    def InitGameTrophyProgress(self, index):
        # 선택한 게임의 진행도 표시
        titleProgress = self.GetGameTrophyProgress(index)

        gameInfoProgress = Label(
            self.gameInfoFrame, text=self.lang_setting['lang_progress'] + " " + str(titleProgress) + "%")
        gameInfoProgress.pack()

        #gameInfoProgress.grid(row=2, column=0)

        return gameInfoProgress
# endregion

# region 게임 정보 위젯 생성
    def CreateAllGameInfoWidgets(self):
        # 게임 정보를 표시할 프레임을 만듦
        self.CreateGameInfoFrame()

        # 각 위젯들을 생성한 후 전역 변수에 대입
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
        self.UpdateSelectedGameInfoDict()
# endregion

# region Specific Menu 전달용 함수
    # specificMenu 스크립트에 넘겨줄 정보를 딕셔너리 형태로 정리하는 함수
    def UpdateSelectedGameInfoDict(self):
        # 게임 이름, 사진, 트로피 현황, 진행도, 선택 언어 정보를 정리 후 넘겨준다.
        selectedGameInfo = {
            'titleName': self.GetGameName(self.currentIndex),
            # PhotoImage 자체를 가져오는 것에 주의
            'titleIcon': self.GetGamePhoto(self.currentIndex),
            'titleTrophyStatus': self.GetGameTrophyStatus(self.currentIndex),
            # 퍼센티지 숫자만 가져오는 것에 주의
            'titleTrophyProgress': self.GetGameTrophyProgress(self.currentIndex),
            'selectedLanguage': self.lang_setting
        }

        return selectedGameInfo

    # 처음 실행할 때 선택된 게임의 정보를 업데이트 하기 위해 한 번 실행
    # UpdateSelectedGameInfoDict()

    # 게임 세부 정보 창을 띄우는 함수
    def ShowGameSpecificInfoWindow(self):
        pass

        #gameInfoDict = UpdateSelectedGameInfoDict()

        #specificWindow = Toplevel(root)

        #specificWindow.title("PS Trophy Manager")
        # specificWindow.geometry("600x750")

        # specificMenu.InitTkRoot(specificWindow)
        # specificMenu.GetGameInfoDict(gameInfoDict)
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
    def __init__(self, root):
        self.root = root
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
