"""
Database class
"""

from pymongo import MongoClient  # Database
from typing import Any

class Database:
    """
    This class will control everything that has to deal with the database
    """

    def __init__(self):
        self.cluster = \
            MongoClient(
                "mongodb+srv://RickShaltz:richardisawesome@cluster0.qggnuii.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["PythonDatabase"]  # add the name of the cluster that was created
        self.user_info = self.db["UserInfo"]  # add the name of the collection under the cluster
        self.online_users = {}

    def create_account(self, account: Any) -> dict[str, any]:
        """
        With a given username and password, attempt to create a user with that information.

        Possible Returns:
        False -> duplicate_username, password_length_invalid, username_length_invalid
        True -> None
        """
        username = account.get_username()
        password = account.get_password()

        same_username_count = self.user_info.count_documents({"_id": username})
        if len(username) <= 0:
            return {"function_to_run": "notify_status_of_account_creation",
                    "parameter": (False, "username_length_invalid")}

        elif same_username_count > 0:
            return {"function_to_run": "notify_status_of_account_creation", "parameter": (False, "duplicate_username")}

        elif len(password) < 3:
            return {"function_to_run": "notify_status_of_account_creation",
                    "parameter": (False, "password_length_invalid")}

        post = {"_id": username, "password": password}
        self.user_info.insert_one(document=post)
        return {"function_to_run": "notify_status_of_account_creation", "parameter": (True, None)}

    def log_in(self, account: Any) -> (str, bool):
        """
        Attempt to log in a user

        Possible returns:
        False -> invalid username, invalid password, already_logged_in
        True -> None
        """
        username = account.get_username()
        password = account.get_password()

        # Check if the username is correct
        username_found = self.user_info.count_documents({"_id": username})
        if username_found == 0:
            return {"function_to_run": "notify_status_of_log_in", "parameter": (False, "invalid_username")}

        # Check if the password and username is correct
        password_found = self.user_info.count_documents({"_id": username, "password": password})
        if password_found == 0:
            return {"function_to_run": "notify_status_of_log_in", "parameter": (False, "invalid_password")}

        if account.get_username() in self.online_users:
            return {"function_to_run": "notify_status_of_log_in", "parameter": (False, "already_logged_in")}

        # add the user to the pool of online users.
        self.online_users[account.get_username()] = account
        # debugging number of online users
        print(f"[Online Users] {self.get_number_of_online_users()}")

        # debugging online users
        for username in self.online_users:
            print(username)

        return {"function_to_run": "notify_status_of_log_in", "parameter": (True, None)}

    def log_out(self, account: Any) -> None:
        """
        Log out an account that has closed the application
        """
        username = account.get_username()
        if username in self.online_users:
            self.online_users.pop(username)

    def get_number_of_online_users(self):
        """Return the number of users online"""
        return len(self.online_users)


"""
# Database Stuff
# post = {"_id": 1, "name": "Alan", "password": "1111"}
# collection.insert_one(document=post)  # add the post to the database
# collection.insert_many([post1, post2]) <- you can insert many posts this way

#results = collection.find({"name": "Richard"})  # this will return a pymongo.cursor object
# collection.find({"ATTRIBUTE TO SEARCH" : "value to find"})
# collection.find({"Attr":"Val", "Attr2":"Val2"})
# collection.find_one({"_id":"val"}) <- returns the first one that it finds

# Loop through all returned results to get each individual one that u need
#for result in results:
#    print(result)

# collection.delete_one({"_id": 0})  # deletes the first one matching this description
# collection.update_one({"_id": 0}, {"$set": {"name": "Awesome Richard"}}) <- u can update the database with this
# https://www.mongodb.com/docs/manual/reference/operator/update/ (Replace $set for what you need)
# $set can also be used to add attributes

#print(collection.count_documents({"_id": 0}))
"""
