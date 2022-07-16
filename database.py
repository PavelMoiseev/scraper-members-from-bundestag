import pymysql
import requests
import json
from bs4 import BeautifulSoup
from config import host, user, password, db_name

DATA_DICT = []


def save_information_in_json():
    with open("members_url_list.txt", "r") as file:
        lines = [line.strip() for line in file]
        # data_dict = []

        for line in lines:
            q = requests.get(line)
            result = q.content

            soup = BeautifulSoup(result, "lxml")
            person = soup.find(class_="col-xs-8 col-md-9 bt-biografie-name").find("h3").text
            person_name_company = person.strip().split(",")
            person_name = person_name_company[0]
            person_company = person_name_company[1].strip()
            social_networks = soup.find_all(class_="bt-link-extern")
            social_networks_urls = []
            for item in social_networks:
                social_networks_urls.append(item.get("href"))

            data = {
                "person_name": person_name,
                "person_company": person_company,
                "social_networks": social_networks_urls
            }

            DATA_DICT.append(data)

        # break_point for testing
            if len(DATA_DICT) == 3:
                break

    with open("members_data.json", "w") as json_file:
        json.dump(DATA_DICT, json_file, indent=4)

    return DATA_DICT


def create_and_populate_data_table():
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                create_table_query_1 = "CREATE TABLE `members` (id INT AUTO_INCREMENT, " \
                                       "member_name VARCHAR(32)," \
                                       "company VARCHAR(32), PRIMARY KEY (id));"
                cursor.execute(create_table_query_1)
                print("Table members created successfully")

            with connection.cursor() as cursor:
                create_table_query_2 = "CREATE TABLE `contacts_members` (id INT AUTO_INCREMENT, " \
                                       "contacts VARCHAR(300), PRIMARY KEY (id)," \
                                       "members_id INTEGER NOT NULL," \
                                       "FOREIGN KEY (members_id) REFERENCES members(id));"
                cursor.execute(create_table_query_2)
                print("Table contacts created successfully")

            with connection.cursor() as cursor:
                for count in range(len(DATA_DICT)):
                    insert_query_1 = ("INSERT INTO `members` (member_name, company) " \
                                    "VALUES ('%(person_name)s', '%(person_company)s')" % {
                                    'person_name': DATA_DICT[count]['person_name'],
                                    'person_company': DATA_DICT[count]['person_company']})

                    cursor.execute(insert_query_1)
                    for item in DATA_DICT[count]['social_networks']:
                        insert_query_2 = ("INSERT INTO `contacts_members` (contacts, members_id) " \
                                        "VALUES ('%(contacts)s', '%(members_id)s')" % {
                                        'contacts': item,
                                        'members_id': count+1})
                        print("done!")
                        cursor.execute(insert_query_2)

                    connection.commit()
                    print("data in table")
        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused")
        print(ex)

    pass
