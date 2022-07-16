from parse_members import save_members_link
from database import save_information_in_json, create_and_populate_data_table

URL_ADDRESS = "https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset="

if __name__ == '__main__':
    save_members_link(URL_ADDRESS)
    save_information_in_json()
    create_and_populate_data_table()



