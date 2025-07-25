from dotenv import load_dotenv
from pymongo import MongoClient
import os
from rich import print

def get_collection():
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    db = client.test
    return db.cats, client

def add_new_cat(collection, name, age, features, owner=None):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    if owner:
        cat["owner"] = owner

    result = collection.insert_one(cat)
    print(f"[green]Кота '{name}' додано з id {result.inserted_id}[/green]")

def get_all_dokuments_in_MongoDB(collection):
    for cat in collection.find():
        print(cat)
    count = collection.count_documents({})
    print(f"[blue bold]Всього котиків у базі:[/blue bold] {count}")


def get_info_of_name_cat(name):
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)

    db = client.test  # доступ до бази 'test' (з конспекту)
    collection = db.cats #доступ до коленкції тест з тогож конспекту

    find_cat = collection.find_one({"name": name})
    if find_cat:
        print(f"[blue bold]Дані про кота:[/blue bold] {find_cat}")
    else:
        print(f"[red bold]Дані про кота не {find_cat} знайдено[/red bold]")
    client.close()

def update_age_of_cat(collection, name, new_age):
    upd_cat = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if upd_cat.modified_count > 0:
        print(f"[green]Вік кота '{name}' оновлено на {new_age} років.[/green]")
    else:
        print(f"[yellow]Кота з ім'ям '{name}' не знайдено або вік уже дорівнює {new_age}.[/yellow]")

def update_features_of_cat(collection, name, new_features):
    features_cat = collection.update_one({"name": name}, {"$push": {"features": new_features}})
    if features_cat.modified_count > 0:
        print(f"[green]Котику '{name}' додано {new_features}.[/green]")
    else:
        print(f"[yellow]Кота з ім'ям '{name}' не знайдено або характеристика {new_features} вже існує.[/yellow]")

def del_cat_by_name(collection, name):
    del_cat = collection.delete_one({"name": name})
    if del_cat.deleted_count > 0:
        print(f"[green]Кота з імям '{name}' видалено з бази.[/green]")
    else:
        print(f"[yellow]Кота з ім'ям '{name}' не знайдено.[/yellow]")

def del_all_cats(collection):
    del_cats = collection.delete_many({})
    print(f"[green]З бази видалено {del_cats.deleted.count}котиків .[/green]")
    





if __name__=="__main__":
    collection, client = get_collection()
    # add_new_cat(collection, "Tom", 6, ["rкучерявий", "кусається"], ["Sasha", 38] )
    get_all_dokuments_in_MongoDB(collection)
    # names = collection.distinct("name")
    # print("[green]Список імен котів:[/green]")
    # for name in names:
    #     print(f"- {name}")
    #     names = collection.distinct("name")
    # cat_name = input("Введіть ім’я кота: ")
    # get_info_of_name_cat(cat_name)
    # update_age_of_cat(collection, "barsik", 5)
    # update_features_of_cat(collection, "Murzik", "Махає хвостом")
    # del_cat_by_name(collection, "barsik")
    client.close()