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

    def create_account(self, account: Any) -> (str, bool):
        """
        With a given username and password, attempt to create a user with that information.
        """
        username = account.get_username()
        password = account.get_password()

        same_username_count = self.user_info.count_documents({"_id": username})
        if same_username_count > 0:
            return {"function_to_run": "notify_status_of_account", "parameter": (False, "duplicate_username")}

        if len(password) < 3:
            return {"function_to_run": "notify_status_of_account", "parameter": (False, "password_length_invalid")}

        post = {"_id": username, "password": password}
        self.user_info.insert_one(document=post)
        return {"function_to_run": "notify_status_of_account", "parameter": (True, None)}


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
