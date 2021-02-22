import requests
import json
from datetime import datetime
from os import path
import os
import argparse
import pprint


# URL args
api_token = 'z9l30RgC5L7GCpiZZ9ix'
order = "created_at"
per_page = 10
now = datetime.now()
created_at_before = now.isoformat()


page_count = 5  # should be 100 requests
company_data = []  # store company data of all pages


def main(country, created_at):
    for i in range(page_count):
        res = requests.get(url=get_url(
            country_code=country, page=i+1, api_token=api_token, created_at=created_at))
        if res.status_code == 200:
            print('response is 200')
            r = res.json()

            companies = r['results']["companies"]
            for company in companies:
                company_data.append(company['company'])
        elif res.status_code == 403 or res.status_code == 503:
            print('daily requests limit exceeds')
            break
        else:
            print(f'response status code: {res.status_code} at page: {i}')
            print(res.text)
            break


def get_url(country_code, api_token, created_at, page, per_page=per_page, order='created_at'):
    return f"https://api.opencorporates.com/companies/search?api_token={api_token}&country_code={country_code}&fields=normalised_name&inactive=false&per_page={per_page}&order={order}&created_at=:{created_at}&page={page}"


def get_last_company_created_date(page):
    '''
    takes a response and returns the last company created_at data
    '''
    return page['results']['companies'][-1]['company']['created_at']


def save_results(country_code):
    file_name = {}
    # loading the config file
    with open('config.json', 'r') as f:
        file_name = json.load(f)

    # checking if the country directory exists
    BASE_DIR = path.dirname(path.abspath(__file__))
    path_ = path.join(BASE_DIR, f'{file_name[country_code]}')

    # creating new directory for given country code
    if not path.exists(path_):
        os.makedirs(path_)

    # saving results in the respective country directory
    with open(f'{file_name[country_code]}/{file_name[country_code]}-{created_at_before}.json', 'w') as f:
        f.write(json.dumps(company_data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument description')
    parser.add_argument('-country', type=str,
                        help='give the country code')
    parser.add_argument('-created_at', type=str,
                        help='crawle data created at before the given date')
    args = parser.parse_args()

    if args.country and args.created_at:
        main(args.country, args.created_at)
        save_results(args.country)
    else:
        print('invalid command!')
        print('sample: ./script.py -country my -created_at 2021-02-22')
