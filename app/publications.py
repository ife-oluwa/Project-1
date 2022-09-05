from scraping import scraping
from sqllite import sqllite_db
import argparse


class publications(object):

    def run(self, total, size_page=48):
        s_d = scraping(total, size_page)
        self.__load_data(s_d.get_data())

    def __load_data(self, data):
        db = sqllite_db('ESTATE')
        db.init_table()
        print("Loading data to database: metroscubicos")
        db.bulk_data(data)
        print(
            f"{db.validate()} records were scraped from metroscubios.com and loaded to metroscubicos")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--total', type=int,
                        help='Total Elements', required=True)
    parser.add_argument('-s', '--size_page', type=int,
                        help='page size', required=False, default=48)
    args = parser.parse_args()
    print(
        f"Getting data from metroscubicos.com, total elements {args.total}, elements per page {args.size_page}")
    publications().run(args.total, args.size_page)
