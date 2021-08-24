from psnawp_api import message_thread
from psnawp_api import psnawp_exceptions


# Class User
# This class will contain the information about the PSN ID you passed in when creating object
class User:
    base_uri = 'https://m.np.playstation.net/api/userProfile/v1/internal/users'

    def __init__(self, request_builder, client, online_id, account_id):
        """
        Constructor of Class User. Creates user object using online id or account id
        :param request_builder: Used to call http requests
        :param client: The user who is logged in. Used to create message threads
        :param online_id:
        :param account_id:
        """
        self.request_builder = request_builder
        self.client = client
        self.online_id = online_id
        self.account_id = account_id
        # If online ID is given search by online ID otherwise by account ID
        if self.online_id is not None:
            profile = self.online_id_to_account_id(online_id)
            self.account_id = profile['profile']['accountId']
        elif self.account_id is not None:
            profile = self.profile()
            self.online_id = profile['onlineId']
        self.msg_thread = None

    def online_id_to_account_id(self, online_id):
        """
        Converts user online ID and returns their account id. This is an internal function and not meant to be called
        directly.

        :param online_id: online id of user you want to search
        :type online_id: str
        :returns: dict: PSN ID and Account ID of the user in search query
        :raises PSNAWPIllegalArgumentError: If the search query is empty
        :raises requests.exception.HTTPError: If the user is not valid/found
        """
        # If user tries to do empty search
        if len(online_id) <= 0:
            raise psnawp_exceptions.PSNAWPIllegalArgumentError('online_id must contain a value.')
        base_uri = "https://us-prof.np.community.playstation.net/userProfile/v1/users"
        param = {'fields': 'accountId,onlineId,currentOnlineId'}
        response = self.request_builder.get(url="{}/{}/profile2".format(base_uri, online_id), params=param)
        return response

    def profile(self):
        """
        Gets the profile of the user

        :returns: Information about profile such as about me, avatars, languages etc...
        :raises requests.exception.HTTPError: If the user is not valid/found
        """
        response = self.request_builder.get(url='{}/{}/profiles'.format(User.base_uri, self.account_id))
        return response

    def get_presence(self):
        """
        Gets the presences of a user. If the profile is private

        :returns: dict availability, lastAvailableDate, and primaryPlatformInfo
        """
        params = {'type': 'primary'}
        response = self.request_builder.get(url='{}/{}/basicPresences'.format(User.base_uri, self.account_id),
                                            params=params)
        if 'basicPresence' in response.keys():
            return response['basicPresence']
        else:
            return response

    # 트로피
    # URL의 기본적인 형태는 https://{platform}.{environment}.playstation.net/api/trophy
    # {platform}에 올 수 있는 것은 ps5, m(모바일), web(웹)
    # {environment}에 올 수 있는 것은 np만 (PSN Network, PSN 계정을 통해 정상적으로 접근하는 방법은 이것밖에 없음)

    # 플레이어의 게임 리스트를 불러옴
    def GetPlayerGames(self):
        """
            Gets games that player has
        """
        # Get games from sony api
        gListURL = "https://m.np.playstation.net/api/trophy/v1/users/{}/trophyTitles".format(self.account_id)
        response = self.request_builder.get(url=gListURL)

        return response

    # URL 설명
    # https://m.np.playstation.net/api/trophy/v1/npCommunicationIds/{npCommunicationId}/trophyGroups/{trophyGroupId}/trophies{?npServiceName=trophy}
    # {npCommunicationId} : 게임 ID(예: 'NPWR20188_00')
    # {trophyGroupId}
    #   default : 본 게임 한 개만 있는 경우
    #   all : 모든 그룹
    #   001, 002, 00n.... : n번째 그룹만 특정
    # {?npServiceName=trophy} : PS3, PS4, PS Vita의 경우에는 꼭 URL 맨 뒤에 붙여야 함

    # 특정 게임의 모든 그룹(또는 특정 그룹)의 모든 트로피 목록을 가져옴
    # 예시
    # GetAllTrophies('NPWR20188_00', 'all')
    def GetAllTrophies(self, npServiceName, npCommunicationId, trophyGroupId):
        # trophy(PS3, PS4, PS Vita)인지 trophy2(PS5)인지 구분
        if(npServiceName == 'trophy'):
            trophyURL = "https://m.np.playstation.net/api/trophy/v1/npCommunicationIds/{}/trophyGroups/{}/trophies?npServiceName=trophy".format(npCommunicationId, trophyGroupId)
        elif(npServiceName == 'trophy2'):
            trophyURL = "https://m.np.playstation.net/api/trophy/v1/npCommunicationIds/{}/trophyGroups/{}/trophies".format(npCommunicationId, trophyGroupId)

        response = self.request_builder.get(url=trophyURL)

        return response

    # URL 설명
    # https://m.np.playstation.net/api/trophy/v1/users/{accountId}/npCommunicationIds/{npCommunicationId}/trophyGroups/{trophyGroupId}/trophies
    # 주의할 점은 유저의 프로필에서 트로피 공개 되어있어야 볼 수 있음
    # {accountId} : 플레이어의 계정ID(npsso code)
    # {npCommunicationId} : 게임 ID(예: 'NPWR20188_00')
    # {trophyGroupId}
    #   default : 본 게임 한 개만 있는 경우
    #   all : 모든 그룹
    #   001, 002, 00n.... : n번째 그룹만 특정
    # {?npServiceName=trophy} : PS3, PS4, PS Vita의 경우에는 꼭 URL 맨 뒤에 붙여야 함

    # 특정 게임의 획득한 트로피 가져오기
    def GetEarnedTrophies(self, npServiceName, npCommunicationId, trophyGroupId):
        # trophy(PS3, PS4, PS Vita)인지 trophy2(PS5)인지 구분
        if(npServiceName == 'trophy'):
            trophyURL = "https://m.np.playstation.net/api/trophy/v1/users/{}/npCommunicationIds/{}/trophyGroups/{}/trophies?npServiceName=trophy".format(self.account_id, npCommunicationId, trophyGroupId)
        elif(npServiceName == 'trophy2'):
            trophyURL = "https://m.np.playstation.net/api/trophy/v1/users/{}/npCommunicationIds/{}/trophyGroups/{}/trophies".format(self.account_id, npCommunicationId, trophyGroupId)

        response = self.request_builder.get(url=trophyURL)

        return response


    # 트로피 레벨 기능
    # https://andshrew.github.io/PlayStation-Trophies/#/APIv2?id=_2-retrieve-the-trophies-for-a-title
    # Trophy Profile Summary 참고

    def friendship(self):
        """
        Gets the friendship status and stats of the user

        :returns: dict: friendship stats
        """
        response = self.request_builder.get(url='{}/me/friends/{}/summary'.format(User.base_uri, self.account_id))
        return response

    def is_available_to_play(self):
        """
        TODO I am not sure what this endpoint returns I'll update the documentation later
        :returns:
        """
        response = self.request_builder.get(url='{}/me/friends/subscribing/availableToPlay'.format(User.base_uri))
        return response

    def is_blocked(self):
        """
        Checks if the user is blocked by you

        :returns: boolean: True if the user is blocked otherwise False
        """
        response = self.request_builder.get(url='{}/me/blocks'.format(User.base_uri))
        if self.account_id in response['blockList']:
            return True
        else:
            return False

    def send_private_message(self, message):
        """
        Send a private message to the user. Due to endpoint limitation. This will only work if the message group
        already exists.

        :param message: body of message
        :type message: str
        """
        if self.msg_thread is None:
            self.msg_thread = message_thread.MessageThread(self.request_builder, self.client, self.online_id)
        self.msg_thread.send_message(message)

    def get_messages_in_conversation(self, message_count=1):
        """
        Gets all the messages in send and received in the message group (Max limit is 200)
        The most recent message will be and the start of list


        :param message_count: The number of messages you want to get
        :type message_count: int
        :returns: message events list containing all messages
        """
        if self.msg_thread is None:
            self.msg_thread = message_thread.MessageThread(self.request_builder, self.client, self.online_id)

        msg_history = self.msg_thread.get_messages(min(message_count, 200))
        return msg_history

    def leave_private_message_group(self):
        """
        If you want to leave the message group
        """
        if self.msg_thread is not None:
            self.msg_thread.leave()

    def __repr__(self):
        return "<User online_id:{} account_id:{}>".format(self.online_id, self.account_id)

    def __str__(self):
        return "Online ID: {} Account ID: {}".format(self.online_id, self.account_id)
