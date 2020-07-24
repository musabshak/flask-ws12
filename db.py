from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017")
db = client.database
favourites = db.favourites


def add_book(book):
    if favourites.count_documents({"_id": book["id"]}, limit=1) == 0:
        book["_id"] = book["id"]
        favourites.insert_one(book)


def delete_book(id):
    favourites.delete_one({"_id": id})


def get_all():
    return favourites.find({})
