import requests
import json
from datetime import datetime
from os import path
import os
import argparse
from multiprocessing import cpu_count, Pool
from itertools import chain

# URL args
API_TOKEN = 'z9l30RgC5L7GCpiZZ9ix'
ORDER = "created_at"
PER_PAGE = 100

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_url(country_code, api_token, created_at, per_page=PER_PAGE, order=ORDER):
    return f"https://api.opencorporates.com/companies/search?api_token={api_token}&country_code={country_code}&fields=normalised_name&inactive=false&per_page={per_page}&order={order}&created_at=:{created_at}"


def start_crawler(url, page):
    res = requests.get(url+f'&page={page}')
    if res.status_code == 200:
        print(f'page: {page}, http: {res.status_code}')
        r = res.json()
        companies = r['results']["companies"]
        current_page = r['results']['page']
        total_page = r['results']['total_pages']
        company_list = []
        for company in companies:
            # adding the page number to the dataset
            company['company']['page'] = current_page
            company['company']['total_pages'] = total_page
            company_list.append(company['company'])
        return company_list
    elif res.status_code == 403 or res.status_code == 503:
        print('daily requests limit exceeds')
        return []
    else:
        print(f'response status code: {res.status_code} at page: {page}')
        print(res.text)
        return []


def main(country, created_at, pages):
    url = get_url(
        country_code=country, api_token=API_TOKEN, created_at=created_at)

    args = ((url, i) for i in range(1, pages+1))
    all_company_list = []
    with Pool() as pool:
        all_company_list = pool.starmap(start_crawler, args)
    return all_company_list


def save_results(country_code, company_list):
    if not company_list:
        print('\nno data is crawled')
        return

    # loading the config file
    file_name = load_config_file()

    # checking if the country directory exists
    BASE_DIR = path.dirname(path.abspath(__file__))
    path_ = path.join(BASE_DIR, f'{file_name[country_code]}')

    # creating new directory for given country code
    if not path.exists(path_):
        os.makedirs(path_)

    # saving results in the respective country directory
    with open(f'{file_name[country_code]}/{file_name[country_code]}-{current_time}.json', 'w') as f:
        f.write(json.dumps(company_list))

    # making a log file
    last_date = company_list[-1]['created_at']
    total_pages = company_list[-1]['total_pages']
    with open('log.txt', 'a') as f:
        f.write(
            f"cmd ran at: {current_time} country_code: {country_code}, total_pages: {total_pages} created_date of last item: {last_date} \n")


def list_unpacker(company_list):
    return list(chain.from_iterable(company_list))


def load_config_file():
    BASE_DIR = path.dirname(path.abspath(__file__))
    path_ = path.join(BASE_DIR, 'config.json')
    if path.exists(path_):
        with open(path_, 'r') as file:
            return json.load(file)
    else:
        raise Exception('config.json file is missing')


def is_validated(country, created_at, pages):
    if country and created_at and pages:
        country_code_list = load_config_file()
        if country not in country_code_list:
            print('invalid country_code')
            return False
        elif int(pages) > 100:
            print('pages value can not exceed 100')
            return False
        else:
            return True
    else:
        print('invalid command!')
        print('sample: python3 script.py -country my -pages 10 -created_at 2021-02-22')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument description')
    parser.add_argument('-country', type=str,
                        help='give the country code')
    parser.add_argument('-created_at', type=str,
                        help='crawle data created at before the given date')
    parser.add_argument('-pages', type=int,
                        help='number pages to be crawled. max value is 100')
    args = parser.parse_args()
    country, created_at, pages = args.country, args.created_at, args.pages

    if is_validated(country, created_at, pages):
        all_company_list = main(country, created_at, pages)
        company_list = list_unpacker(all_company_list)
        save_results(args.country, company_list)
