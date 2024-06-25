import random
import requests
import time


# info about your user (necessary for data scraping with instagram APIs)
print("\nIn order to get the following info you need to intercept http requests after you logged into your ig account (use Burp Suite)\n\n")
userID=input("Enter your userID ('/api/v1/friendships/USERID/following' OR param 'ds_user_id'): ")
sessionid=input("Enter your sessionid (cookie 'sessionid'): ")
XIgAppId=input("Enter your X-Ig-App-Id (header 'X-Ig-App-Id'): ")


maxUnfollowerFollowers = input("Minimum unfollower's followers (void/literal=no filtering): ")
if(maxUnfollowerFollowers.isnumeric()):
    maxUnfollowerFollowers = int(maxUnfollowerFollowers)
else:
    maxUnfollowerFollowers=-1


followingIDs = []
followersIDs = []
unfollowingUsername = []


# collecting ids of every following user
print("Checking for followers and followings...")
r = requests.get(f"https://www.instagram.com/api/v1/friendships/{userID}/following/", headers={
    "Cookie": f"ds_user_id={userID}; sessionid={sessionid}",
    "X-Ig-App-Id": XIgAppId
})
res = r.json()
for item in res["users"]:
    followingIDs.append(item["id"])
while(res["page_size"]!=0):
    r = requests.get(f"https://www.instagram.com/api/v1/friendships/{userID}/following/?max_id={len(followingIDs)}", headers={
        "Cookie": f"ds_user_id={userID}; sessionid={sessionid}",
        "X-Ig-App-Id": XIgAppId
    })
    res = r.json()      # getting json about following users
    for item in res["users"]:
        followingIDs.append(item["id"])


# collecting ids of every follower
r = requests.get(f"https://www.instagram.com/api/v1/friendships/{userID}/followers/", headers={
    "Cookie": f"ds_user_id={userID}; sessionid={sessionid}",
    "X-Ig-App-Id": XIgAppId
})
res = r.json()
nextMaxId = res["next_max_id"]
for item in res["users"]:
    followersIDs.append(item["id"])
while "next_max_id" in res:
    r = requests.get(f"https://www.instagram.com/api/v1/friendships/{userID}/followers/?max_id={nextMaxId}", headers={
        "Cookie": f"ds_user_id={userID}; sessionid={sessionid}",
        "X-Ig-App-Id": XIgAppId
    })
    res = r.json()      # getting json about follower users
    if "next_max_id" in res:
        nextMaxId = res["next_max_id"]
    for item in res["users"]:
        followersIDs.append(item["id"])


print("\nTotal following:", len(followingIDs))
print("Total followers:", len(followersIDs))
print("Checking for unfollowers...")

# checking if every following are follower
for x in followingIDs:
    if x not in followersIDs:
        r = requests.get(f"https://www.instagram.com/api/v1/users/{x}/info/",
                         headers={
                             "Cookie": f"ds_user_id={userID}; sessionid={sessionid}",
                             "X-Ig-App-Id": XIgAppId
                         })
        res = r.json()

        # reporting a following which is not a follower
        if (not (int(res["user"]["follower_count"]) > maxUnfollowerFollowers)) or maxUnfollowerFollowers==-1:
            print("\nunfollower found!\nid:", x)
            print("username:", res["user"]["username"])
            unfollowingUsername.append(res["user"]["username"])
        time.sleep(random.randint(2,6))     # avoid stressing instagram servers

print("\nTotal unfollowers:", len(unfollowingUsername))
print("Unfollower list: ")
for item in unfollowingUsername:
    print("\t", item)
