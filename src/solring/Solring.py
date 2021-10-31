import solr
import sys
import argparse

from pandas import DataFrame


class Solring:

    def __init__(self, url, core, qt=None):
        assert url is not None, "url must be a valid solr path"
        assert core is not None, "core must be a valid solr core name"

        self.url = url
        self.qt = qt
        self.core = core

    def execute(self, params: dict, output: str, save_format: str):
        solr_connection = solr.Solr(f"{self.url + '/solr/' + self.core}",
                                    persistent=False,
                                    timeout=360,
                                    max_retries=1)
        search_handler = solr.SearchHandler(solr_connection, self.qt)

        response = search_handler(
            fields=params.get('fl'),
            **params
        )

        assert response is not None, "response is None"

        file_name = f"{output}.{save_format}"
        DataFrame(response.results).to_csv(path_or_buf=file_name, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='solring 0.0.1')
    parser.add_argument("--url", "-u", required=True, help="The host:port of the running solr", type=str)
    parser.add_argument("--output", "-o", required=False, default='output', help="Output file name", type=str)
    parser.add_argument("--save_format", "-sf", required=False, default='txt', help="File type of saved records",
                        choices=['csv', 'txt'])
    parser.add_argument("--core", "-c", required=True, help="The core/collection in solr", type=str)
    parser.add_argument("--rows", "-r", required=False, help="The number of row numbers returned", default=5, type=int)
    parser.add_argument("-fl", required=False, default='id', help="Field list to retrieve", type=str)
    parser.add_argument("-q", required=False, default="*:*", help="Search query", type=str)
    parser.add_argument("-fq", required=False, action='append', help="Filter queries", type=str)
    parser.add_argument("--score", required=False, action='store_true', help="Learn score of each record")
    parser.add_argument("--qt", default='/select', required=False, type=str,
                        help="solr request handle to query on, default is '/select'")

    args = parser.parse_args(sys.argv[1:])

    solr_params = {
        'q': args.q,
        'wt': "json",
        'rows': args.rows,
        'score': args.score,
        'fl': args.fl
    }
    if args.fq:
        solr_params['fq'] = args.fq

    solring = Solring(args.url, args.core, args.qt)
    solring.execute(solr_params, output=args.output, save_format=args.save_format)


if __name__ == '__main__':
    main()
