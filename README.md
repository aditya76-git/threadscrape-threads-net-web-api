

![Logo](https://i.imgur.com/OPzvKEZ.png)
<div style="text-align:center;">
  <a href="https://github.com/aditya76-git">aditya76-git</a> /
  <a href="https://github.com/aditya76-git/threadscrape-threads-net-web-api">threadscrape-threads-net-web-api</a>
</div>

<br />

<!-- <img src="https://i.imgur.com/y3L6XfN.png" align="right" /> -->

# ThreadScrape - Threads.net WEB-API
Access Account Information, User Details, Search Content with ThreadScrape



## 📋Details

- 👤 USER
  - [Get User ID](#get-user-id)
  - [Get Profile Info](#get-profile-info)
  - [Get Followers](#get-followers)
  - [Get Following](#get-following)
  - [Get User Profile Threads](#get-user-profile-threads)
  - [Get Recommended User](#get-recommended-user)

- 📝 POST
  - [Get Post Info](#get-post-info)
  - [Get Post Media](#get-post-media)

- 🔍 SEARCH
  - [Search](#search)

- ⚙️ ACTIONS
  - [Follow User](#follow-user)
  - [UnFollow User](#unfollow-user)
  - [Block User](#block-user)
  - [UnBlock User](#unblock-user)
  - [Like Post](#like-post)
  - [UnLike Post](#unlike-post)
  - [Create Thread](#create-thread)
  - [Delete Thread](#delete-thread)
  - [Update Reply Permission](#update-reply-permission)

## ⚠️ Disclaimer

Please note that the `threadscrape` package is provided as-is and is not officially endorsed or supported by `Threads`. While we have taken care to ensure that the package interacts with the Threads API in a secure and compliant manner, we cannot guarantee the safety of your Threads account.

By using the `threadscrape` package, you acknowledge and agree that you are responsible for any actions taken with your Threads account, and you use the package at your own risk. We recommend using the package responsibly

We are not liable for any potential consequences that may arise from using the `threadscrape` package, including but not limited to `account suspension`, `data loss`, or any other `issues` related to your `Threads` account.

It's important to exercise `caution` and ensure that you keep your `sensitive information`, such as the `sessionid` , `fb_dtsg` , `csrftoken` cookie, `private` and `secure`. If you have any concerns or questions, please refer to the documentation or seek assistance from the community.



## ⚙️Installation

Open your terminal or command prompt and enter the following command:



```bash
pip install git+https://github.com/aditya76-git/threadscrape-threads-net-web-api@main
```
> **Note:** To use threadscrape you need to have a Active Threads Account 

## 🚀 Initialization

To get started with ThreadScrape, you'll need to initialize an instance of the `ThreadScrape` class by passing your user session data as an argument. Make sure to replace `"your_session_id"`, `"your_fb_dtsg"`, and `"your_csrftoken"` with your actual session data.

```python
from threadscrape import ThreadScrape

# Your user session data
session_data = {
    "sessionid": "your_session_id",
    "fb_dtsg": "your_fb_dtsg",
    "x-csrftoken": "your_csrftoken"
}

# Initialize a ThreadScrape instance
api = ThreadScrape(session_data)
```

## 📌 Note

Every time you log in with your Threads account, the previous session data expires. This means that any session values obtained during a previous login session, such as `sessionid`, `fb_dtsg`, and `x-csrftoken`, will no longer work. Make sure to update these values with the latest session data after each login to ensure `ThreadScrape` continue to function correctly.

LogIn Once and obtain the session data and don't logout. If you will logout you will have to update session data again



## 🔍 How to Find sessionid and csrftoken cookie?

- `sessionid` and `csrftoken` cookie is required to authenticate against `Threads` in order to have access to the required services.
- Using any extensions like `Cookie-Editor` can easily help you find it
- [Extension Link - Chrome WEB Store](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

![Finding the sessionid Cookie Value](https://i.imgur.com/9CrGIkQ.png "Finding the sessionid Cookie Value")
![Finding the csrftoken Cookie Value](https://i.imgur.com/EPZ23tZ.png "Finding the csrftoken Cookie Value")


> **Note:** While cookies can contain sensitive information, the sessionid and csrftoken cookie value is required for authentication and direct communication with the Threads API within the scope of this open-source project. Rest assured that your cookies will not be sent to any external server; it is solely used for interacting with Thread's services through the project's codebase. However, caution is advised when sharing this cookie value outside the context of this project, as it could potentially lead to unauthorized access to your Threads account.


## 🔍 How to Find fb_dtsg payload value
[STEP BY STEP GUIDE](https://graph.org/How-to-Find-Your-fb-dtsg-Payload-Value-09-10)

<a href="https://graph.org/How-to-Find-Your-fb-dtsg-Payload-Value-09-10">
  <img src="https://i.imgur.com/DgY0plu.png" alt="Finding the fb_dtsg Payload Value">
</a>

## 👤 USER

#### <a id="get-user-id"></a>➡️ Get UserID

```python3
api.get_user_id(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user. | thedankoe |

Returns:
- int: The user ID.


#### <a id="get-profile-info"></a>➡️ Get Profile Info

```python3
api.get_profile_info(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user. | thedankoe |

Returns:
- dict: A JSON response containing profile information.


#### <a id="get-followers"></a>➡️ Get Followers

```python3
api.get_followers(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user. | thedankoe |

Returns:
- dict: A JSON response containing Followers information.


#### <a id="get-following"></a>➡️ Get Following

```python3
api.get_following(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user. | thedankoe |

Returns:
- dict: A JSON response containing Following information.


#### <a id="get-user-profile-threads"></a>➡️ Get User Profile Threads

```python3
api.get_user_profile_threads(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user. | thedankoe |

Returns:
- dict: A JSON response containing threads associated with a user's profile.


#### <a id="get-recommended-user"></a>➡️ Get Recommended User

```python3
api.get_recommended_users(limit=10)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `limit` | `int` | **Optional**. The maximum number of recommended users to retrieve (default is 20). | 10 |

Returns:
- dict: A JSON response containing recommended Threads users to follow.


## 📝 POST

#### <a id="get-post-info"></a>➡️ Get Post Info

```python3
api.get_post_info(postURL)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `postURL` | `str` | **Required**. The url of the post to get info for. | https://www.threads.net/@r2recody/post/CxAMlXULQ54 |

Returns:
- int: The user ID.


#### <a id="get-post-media"></a>➡️ Get Post Media

```python3
api.get_post_media(postURL)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `postURL` | `str` | **Required**. The url of the post to get media for. | https://www.threads.net/@codeforreal/post/Cw-P6KtvtUD |
| `image_size` | `str` | **Optional**. Image Size if available | 640 |

Note: 
- For a post having images it will return JSON including all available images
- For a post having videos it will return JSON including the thumbnail of all available videos

Returns:
- dict: A JSON containing Media Info (Images and Videos)



## 🔍 SEARCH
#### <a id="search"></a>➡️ Search

```python3
api.search(query , limit=10)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `query` | `str` | **Required**. The search query. | zuck |
| `limit` | `str` | **Optional**. The maximum number of results to return (default is 10). | 10 |

Returns:
- dict: A JSON response containing search information.


## ⚙️ ACTIONS
#### <a id="follow-user"></a>➡️ Follow User

```python3
api.follow_user(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user to follow. | zuck |


Returns:
- dict: A JSON response confirming the follow action.

#### <a id="unfollow-user"></a>➡️ UnFollow User

```python3
api.unfollow_user(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user to unfollow. | zuck |


Returns:
- dict: A JSON response confirming the unfollow action.

#### <a id="block-user"></a>➡️ Block User

```python3
api.block_user(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user to block. | zuck |


Returns:
- dict: A JSON response confirming the block action.

#### <a id="unblock-user"></a>➡️ UnBlock User

```python3
api.unblock_user(username)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `username` | `str` | **Required**. The username or profile URL of the user to unblock. | zuck |


Returns:
- dict: A JSON response confirming the unblock action.


#### <a id="like-post"></a>➡️ Like Post

```python3
api.like_post(postURL)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `postURL` | `str` | **Required**. The URL of the post to like. | https://www.threads.net/@zuck/post/Cwm6qX_LL_M |

Returns:
- dict: A JSON response confirming the like action.



#### <a id="unlike-post"></a>➡️ UnLike Post

```python3
api.unlike_post(postURL)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `postURL` | `str` | **Required**. The URL of the post to unlike. | https://www.threads.net/@zuck/post/Cwm6qX_LL_M |


Returns:
- dict: A JSON response confirming the unlike action.


#### <a id="create-thread"></a>➡️ Create Thread

```python3
api.create_thread(text)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `text` | `str` | **Required**. The text content of the thread. | Hello World Posting from ThreadScrape |


Returns:
- dict: A JSON response containing the Thread Info.


#### <a id="delete-thread"></a>➡️ Delete Thread

```python3
api.delete_thread(postURL)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `postURL` | `str` | **Required**. The URL of the thread to delete. | url |


Returns:
- dict: A JSON response confirming the thread deletion.


#### <a id="update-reply-permission"></a>➡️ Update Reply Permission

```python3
api.update_reply_permission(postURL, option = "your_followers")
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `postURL` | `str` | **Required**. The URL of the thread to delete. | url |
| `option` | `str` | **Optional**. The reply permission option (default is "accounts_you_follow"). Available Options are mentioned_only, your_followers and accounts_you_follow | your_followers |


Returns:
- dict: A JSON response confirming the update.



## 🌟 Show Your Support

- If you find this project useful or interesting, please consider giving it a star on GitHub. It's a simple way to show your support and help others discover the project.


![Github Stars](https://img.shields.io/github/stars/aditya76-git/threadscrape-threads-net-web-api?style=social "Github Stars")

## 👨‍💻Developement

Thank you for your interest in contributing to this project! There are several ways you can get involved:

- **Opening Issues**: If you encounter a bug, have a feature request, or want to suggest an improvement, please open an issue. We appreciate your feedback!
- **Cloning the Project**: To work on the project locally, you can clone the repository by running:
```bash
git clone https://github.com/aditya76-git/threadscrape-threads-net-web-api.git
```
- **Sending Pull Requests**: If you'd like to contribute directly to the codebase, you can fork the repository, make your changes, and then send a pull request. We welcome your contributions!




## 💻Authors

- Copyright © 2023 - [aditya76-git](https://github.com/aditya76-git) / [threadscrape-threads-net-web-api](https://github.com/aditya76-git/threadscrape-threads-net-web-api)
