import requests, re, json
from .errors import ThreadScrapeError
from .utils import get_json_response, arrange_media_data


class ThreadScrape:
    """
    A class for scraping data from the Threads.net WEB-API.
    """

    def __init__(self, data):
        """
        Initializes a ThreadScrape instance with user data.

        Args:
            data (dict): A dictionary containing user session data with keys 'sessionid', 'fb_dtsg', and 'x-csrftoken'.
                These are required for making authenticated requests.
        """
        self.session = requests.Session()
        self.BASE_URL = "https://www.threads.net"
        self.GRAPHQL_URL = "https://www.threads.net/api/graphql"
        self.lsd_token = "AVqw_XEyRAI"
        self.common_headers = self.get_common_headers()
        self.setup_credentials(data)
        self.setup_headers()

    def get_common_headers(self):
        """
        Get common HTTP headers used in requests.

        Returns:
            dict: A dictionary containing common HTTP headers.
        """
        return {
            "authority": self.BASE_URL,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en,en-US;q=0.9,en-IN;q=0.8",
            "cache-control": "max-age=0",
            "dpr": "1.5",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-full-version-list": '"Chromium";v="116.0.5845.180", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.180"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "viewport-width": "1280",
        }


    def setup_credentials(self, data):
        """
        Set up user credentials for the session.

        Args:
            data (dict): A dictionary containing user session data.

        Raises:
            ValueError: If required keys are missing or data format is invalid.
        """
        # Check if all required keys are present
        required_keys = ["sessionid", "fb_dtsg", "x-csrftoken"]
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            raise ValueError(f"Missing keys: {', '.join(missing_keys)}")

        # Check if values are in the expected format
        if not isinstance(data["sessionid"], str) or not isinstance(data["fb_dtsg"], str) or not isinstance(data["x-csrftoken"], str):
            raise ValueError("Invalid data format")

        self.sessionid = data["sessionid"]
        self.fb_dtsg = data["fb_dtsg"]
        self.x_csrftoken = data["x-csrftoken"]

    def setup_headers(self):
        """
        Set up HTTP headers for the session.
        """
        self.session.cookies.update({"sessionid": self.sessionid})
        self.session.headers.update(
            {
                "authority": "www.threads.net",
                "accept": "*/*",
                "accept-language": "en,en-US;q=0.9,en-IN;q=0.8",
                "content-type": "application/x-www-form-urlencoded",
                "dpr": "1.5",
                "origin": "https://www.threads.net",
                "sec-ch-prefers-color-scheme": "dark",
                "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                "sec-ch-ua-full-version-list": '"Chromium";v="116.0.5845.180", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.180"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-model": '""',
                "sec-ch-ua-platform": '"Windows"',
                "sec-ch-ua-platform-version": '"15.0.0"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                "x-asbd-id": "129477",
                "x-fb-lsd": self.lsd_token,
                "x-ig-app-id": "238260118697367",
            }
        )

    def get_user_id(self, url):
        """
        Get the user ID from a Threads.net profile URL or username.

        Args:
            url (str): The profile URL or username.

        Returns:
            int: The user ID.

        Raises:
            ThreadScrapeError: If there's an error retrieving the user ID.
        """
        if "https" in url:
          pattern = r'https://www\.threads\.net/@([^/]+)'
          username = re.search(pattern, url).group(1)
        else:
          username = url

        headers = self.get_common_headers()

        response = requests.get(
            "{}/@{}".format(self.BASE_URL, username), headers=headers
        ).text

        pattern = r'"userID":"(\d+)"'
        match = re.search(pattern, response)

        if match:
            user_id = match.group(1)
        else:
            raise ThreadScrapeError("Error Retriving userID")

        return int(user_id)

    def get_post_id(self, url):
        """
        Get the post ID from a Threads.net post URL.

        Args:
            url (str): The post URL.

        Returns:
            str: The post ID.

        Raises:
            ThreadScrapeError: If there's an error retrieving the post ID.
        """
        headers = self.get_common_headers()

        response = self.session.get(url, headers=headers).text


        pattern = r'"postID":"(\d+)"'
        match = re.search(pattern, response)

        if match:
            post_id = match.group(1)
        else:
            raise ThreadScrapeError("Error Retriving postID")

        return post_id

    def get_id(self, url):
        """
        Get the ID from a Threads.net URL.

        Args:
            url (str): The URL.

        Returns:
            str: The ID.

        Raises:
            ThreadScrapeError: If there's an error retrieving the ID.
        """
        headers = self.get_common_headers()


        response = self.session.get(url, headers=headers).text


        pattern = r'"id":"(\d+_\d+)"'
        match = re.search(pattern, response)

        if match:
            id = match.group(1)
        else:
            raise ThreadScrapeError("Error Retriving ID")

        return id


    def get_followers(self, username):
        """
        Get the Followers from a Threads.net profile URL or username.

        Args:
            username (str): The profile URL or username.

        Returns:
            dict: Get the Followers from a Threads.net profile URL or username.

        Raises:
            ThreadScrapeError: If there's an error retrieving the user ID.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'BarcelonaFriendshipsFollowersTabQuery'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'lsd': 'nucUUd7UtYh-1Efz-5wTiC',
            'fb_api_req_friendly_name': 'BarcelonaFriendshipsFollowersTabQuery',
            'variables': '{{"userID":"{}","__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true}}'.format(userID),
            'server_timestamps': 'true',
            'doc_id': "6173206472779164",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error retrieving Followers for {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json

    def get_following(self, username):
        """
        Get the user's following data

        Args:
            username (str): The username or profile URL of the user.

        Returns:
            dict: A JSON response containing following data.

        Raises:
            ThreadScrapeError: If there's an error retrieving following data.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'BarcelonaFriendshipsFollowingTabQuery'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'lsd': 'nucUUd7UtYh-1Efz-5wTiC',
            'fb_api_req_friendly_name': 'BarcelonaFriendshipsFollowingTabQuery',
            'variables': '{{"userID":"{}","__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true}}'.format(userID),
            'server_timestamps': 'true',
            'doc_id': "6566004623483043",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error retrieving Followers for username {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json

    def follow_user(self, username):
        """
        Follow a Threads.net user.

        Args:
            username (str): The username or profile URL of the user to follow.

        Returns:
            dict: A JSON response confirming the follow action.

        Raises:
            ThreadScrapeError: If there's an error while attempting to follow the user.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaFollowMutationFollowMutation'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'lsd': 'BSWpx6WGeZ94S2rNbmkxn4',
            'fb_api_req_friendly_name': 'useBarcelonaFollowMutationFollowMutation',
            'variables': '{{"target_user_id":"{}"}}'.format(userID),
            'server_timestamps': 'true',
            'doc_id': "6240353742756860",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Following User {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json

    def unfollow_user(self, username):
        """
        Unfollow a Threads.net user.

        Args:
            username (str): The username or profile URL of the user to unfollow.

        Returns:
            dict: A JSON response confirming the unfollow action.

        Raises:
            ThreadScrapeError: If there's an error while attempting to unfollow the user.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaFollowMutationUnfollowMutation'})

        data = {
          'fb_dtsg': self.fb_dtsg,
          'lsd': 'BSWpx6WGeZ94S2rNbmkxn4',
          'fb_api_req_friendly_name': 'useBarcelonaFollowMutationUnfollowMutation',
          'variables': '{{"target_user_id":"{}"}}'.format(userID),
          'server_timestamps': 'true',
          'doc_id': "6419596478124270",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error UnFollowing User {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json

    def like_post(self, postURL):
        """
        Like a Threads.net post.

        Args:
            postURL (str): The URL of the post to like.

        Returns:
            dict: A JSON response confirming the like action.

        Raises:
            ThreadScrapeError: If there's an error while attempting to like the post.
        """
        postID = self.get_post_id(postURL)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaLikeMutationLikeMutation'})

        data = {

            'fb_dtsg': self.fb_dtsg,
            'lsd': 'OacJH75YYKAh8Xtd4UtEJT',
            'fb_api_req_friendly_name': 'useBarcelonaLikeMutationLikeMutation',
            'variables': '{{"media_id":"{}"}}'.format(postID),
            'server_timestamps': 'true',
            'doc_id': "6163527303756305",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Liking Post"

        r_json = get_json_response(response, error_message)

        return r_json

    def unlike_post(self, postURL):
        """
        Unlike a Threads.net post.

        Args:
            postURL (str): The URL of the post to unlike.

        Returns:
            dict: A JSON response confirming the unlike action.

        Raises:
            ThreadScrapeError: If there's an error while attempting to unlike the post.
        """
        postID = self.get_post_id(postURL)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaLikeMutationUnlikeMutation'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'fb_api_req_friendly_name': 'useBarcelonaLikeMutationUnlikeMutation',
            'variables': '{{"media_id":"{}"}}'.format(postID),
            'server_timestamps': 'true',
            'doc_id': "6574229129305381",
        }


        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error UnLiking Post"

        r_json = get_json_response(response, error_message)

        return r_json


    def get_profile_info(self, username):
        """
        Get profile information for a Threads.net user.

        Args:
            username (str): The username or profile URL of the user.

        Returns:
            dict: A JSON response containing profile information.

        Raises:
            ThreadScrapeError: If there's an error retrieving profile information.
        """
        self.session.headers.update({'x-fb-friendly-name': 'BarcelonaUsernameHoverCardImplQuery'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'fb_api_req_friendly_name': 'BarcelonaUsernameHoverCardImplQuery',
            'variables': '{{"username":"{}"}}'.format(username),
            'server_timestamps': 'true',
            'doc_id': "6294229744032325",
        }


        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Retriving Profile Details"

        r_json = get_json_response(response, error_message)

        return r_json

    def search(self, query, limit=10):
        """
        Search for users on Threads.net.

        Args:
            query (str): The search query.
            limit (int, optional): The maximum number of results to return (default is 10).

        Returns:
            dict: A JSON response containing search results.

        Raises:
            ThreadScrapeError: If there's an error while performing the search.
        """
        limit = int(limit)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaAccountSearchGraphQLDataSourceQuery'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'fb_api_req_friendly_name': 'useBarcelonaAccountSearchGraphQLDataSourceQuery',
            'variables': '{{"query":"{}","first":{},"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true}}'.format(query, limit),
            'server_timestamps': 'true',
            'doc_id': "6427333243987367",
        }


        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Searching"

        r_json = get_json_response(response, error_message)

        return r_json


    def get_recommended_users(self, limit=20):
        """
        Get recommended Threads.net users to follow.

        Args:
            limit (int, optional): The maximum number of recommended users to retrieve (default is 20).

        Returns:
            dict: A JSON response containing recommended user data.

        Raises:
            ThreadScrapeError: If there's an error retrieving recommended users.
        """
        self.session.headers.update({'x-fb-friendly-name': 'BarcelonaSearchRecommendedUsersRefetchableQuery'})

        data = {
            'fb_dtsg': self.fb_dtsg,
            'fb_api_req_friendly_name': 'BarcelonaSearchRecommendedUsersRefetchableQuery',
            'variables': '{{"after":"{}","before":null,"first":10,"last":null,"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true}}'.format(limit),
            'server_timestamps': 'true',
            'doc_id': "6476698865784411",
        }


        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Retriving Profile Details"

        r_json = get_json_response(response, error_message)

        return r_json

    def create_thread(self, text):
        """
        Create a new Threads.net thread (text post).

        Args:
            text (str): The text content of the thread.

        Returns:
            dict: A JSON response confirming the thread creation.

        Raises:
            ThreadScrapeError: If there's an error while creating the thread.

        Note: Only this method requires the x-csrftoken in order to create post
        """
        self.session.headers.update({'x-csrftoken': self.x_csrftoken})
        data = {
            'caption': text,
            'is_meta_only_post': '',
            'is_paid_partnership': '',
            'publish_mode': 'text_post',
            'text_post_app_info': '{"reply_control":0}',
          }

        response = self.session.post(
            '{}/api/v1/media/configure_text_only_post/'.format(self.BASE_URL), data=data,
         )

        error_message = "Error Creating Thread"

        r_json = get_json_response(response, error_message)

        return r_json

    def update_reply_permission(self, postURL, option="accounts_you_follow"):
        """
        Update the reply permission of a Threads.net post.

        Args:
            postURL (str): The URL of the post to update.
            option (str, optional): The reply permission option (default is "accounts_you_follow"). Available Options are mentioned_only, your_followers and accounts_you_follow

        Returns:
            dict: A JSON response confirming the update.

        Raises:
            ThreadScrapeError: If there's an error while updating the reply permission.
        """
        postID = self.get_post_id(postURL)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaSetPostReplyControlMutation'})
        # mentioned_only, accounts_you_follow, your_followers

        data = {
            'fb_dtsg': self.fb_dtsg,
            'fb_api_req_friendly_name': 'useBarcelonaSetPostReplyControlMutation',
            'variables': '{{"reply_control":"{}","post_id":"{}"}}'.format(option, postID),
            'server_timestamps': 'true',
            'doc_id': "6476698865784411",
        }


        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Updating Reply Permission"

        r_json = get_json_response(response, error_message)

        return r_json


    def delete_thread(self, postURL):
        """
        Delete a Threads.net thread.

        Args:
            postURL (str): The URL of the thread to delete.

        Returns:
            dict: A JSON response confirming the thread deletion.

        Raises:
            ThreadScrapeError: If there's an error while deleting the thread.
        """
        id = self.get_id(postURL)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaDeleteMutationMutation'})

        data = {
                'fb_dtsg': self.fb_dtsg,
                'fb_api_req_friendly_name': 'useBarcelonaDeleteMutationMutation',
                'variables': '{{"media_id":"{}"}}'.format(id),
                'server_timestamps': 'true',
                'doc_id': "9722027491203611",
            }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Deleting Thread"

        r_json = get_json_response(response, error_message)

        return r_json

    def block_user(self, username):
        """
        Block a Threads.net user.

        Args:
            username (str): The username or profile URL of the user to block.

        Returns:
            dict: A JSON response confirming the block action.

        Raises:
            ThreadScrapeError: If there's an error while blocking the user.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaUserBlockMutation'})

        data = {
          'fb_dtsg': self.fb_dtsg,
          'lsd': 'BSWpx6WGeZ94S2rNbmkxn4',
          'fb_api_req_friendly_name': 'useBarcelonaUserBlockMutation',
          'variables': '{{"user_id":"{}"}}'.format(userID),
          'server_timestamps': 'true',
          'doc_id': "7159968810697379",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error Blocking User {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json

    def unblock_user(self, username):
        """
        Unblock a Threads.net user.

        Args:
            username (str): The username or profile URL of the user to unblock.

        Returns:
            dict: A JSON response confirming the unblock action.

        Raises:
            ThreadScrapeError: If there's an error while unblocking the user.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'useBarcelonaUserUnblockMutation'})

        data = {
          'fb_dtsg': self.fb_dtsg,
          'lsd': 'BSWpx6WGeZ94S2rNbmkxn4',
          'fb_api_req_friendly_name': 'useBarcelonaUserUnblockMutation',
          'variables': '{{"user_id":"{}"}}'.format(userID),
          'server_timestamps': 'true',
          'doc_id': "6572924756096893",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error UnBlocking User {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json

    def get_user_profile_threads(self, username):
        """
        Get the Threads.net threads associated with a user's profile.

        Args:
            username (str): The username or profile URL of the user.

        Returns:
            dict: A JSON response containing user profile threads.

        Raises:
            ThreadScrapeError: If there's an error retrieving user profile threads.
        """
        userID = self.get_user_id(username)

        self.session.headers.update({'x-fb-friendly-name': 'BarcelonaProfileThreadsTabQuery'})

        data = {
          'fb_dtsg': self.fb_dtsg,
          'lsd': 'BSWpx6WGeZ94S2rNbmkxn4',
          'fb_api_req_friendly_name': 'BarcelonaProfileThreadsTabQuery',
          'variables': '{{"userID":"{}"}}'.format(userID),
          'server_timestamps': 'true',
          'doc_id': "6232751443445612",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error retrieving Threads for {}".format(username)

        r_json = get_json_response(response, error_message)

        return r_json


    def get_post_info(self, postURL):
        """
        Get the Info for Thread Post.

        Args:
            postURL (str): postURL to get the info for

        Returns:
            dict: A JSON response containing thread's post

        Raises:
            ThreadScrapeError: If there's an error retrieving post.
        """
        postID = self.get_post_id(postURL)

        self.session.headers.update({'x-fb-friendly-name': 'BarcelonaPostPageQuery'})

        data = {
          'fb_dtsg': self.fb_dtsg,
          'lsd': 'SI3IPQlJXR0BOvV0HaHVtY',
          'fb_api_req_friendly_name': 'BarcelonaPostPageQuery',
          'variables': '{{"postID":"{}","__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaIsFeedbackHubEnabledrelayprovider":false}}'.format(postID),
          'server_timestamps': 'true',
          'doc_id': "6994920940542386",
        }

        response = self.session.post(self.GRAPHQL_URL, data=data)

        error_message = "Error retrieving Post Info for {}".format(postURL)

        r_json = get_json_response(response, error_message)

        return r_json
    

    def get_post_media(self, postURL, image_size="original"):
        post_info = self.get_post_info(postURL)
        media = arrange_media_data(post_info, image_size=image_size)

        return media