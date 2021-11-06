import solr
import sys
import argparse

from pandas import DataFrame, concat


class Solring:

    def __init__(self, url, core, qt=None):
        assert url is not None, "url must be a valid solr path"
        assert core is not None, "core must be a valid solr core name"

        self.url = url
        self.qt = qt
        self.core = core

    def next_batch(self, handler, response, _params):
        """
        Load the next set of matches.
        """
        assert response is not None, "response is None"

        try:
            start = int(response.results.start)
        except AttributeError:
            start = 0

        start += len(response.results)
        _params['start'] = start
        return handler(
            fields=_params.get('fl'),
            **_params
        )

    def execute(self, params: dict, gparams: dict, output: str, save_format: str):
        """
        Query Solr request
        :param params: the solr request parameters
        :param gparams: the group request parameters
        :param output: when records will be saved to a file, output is used.
        :param save_format: the saved file format
        """
        solr_connection = solr.Solr(f"{self.url + '/solr/' + self.core}",
                                    persistent=False,
                                    timeout=360,
                                    max_retries=1)
        search_handler = solr.SearchHandler(solr_connection, self.qt)

        response = search_handler(
            fields=params.get('fl'),
            **params
        )
        assert response is not None, "solr response is not valid"
        print(f"{response.numFound} records found.")
        if response.numFound == 0:
            sys.exit(0)

        result_list = [DataFrame(response.results)]
        response = self.next_batch(search_handler, response, params)
        while response:
            print(f"retrieve next {params.get('rows')} batches at {response.results.start}")
            result_list.append(DataFrame(response.results))
            response = self.next_batch(search_handler, response, params)

        self.save_data(output, params, gparams, result_list, save_format)

    def save_data(self, output, params, gparams, result_list, save_format):
        file_name = f"{output}.{save_format}"
        if gparams.get('param_group_by', False):
            agg_dict = {
                field: gparams['param_group_agg'] for field in gparams['param_group_column']
            }
            concat(result_list) \
                .groupby(gparams['param_group_fl']) \
                .agg(agg_dict) \
                .reset_index(drop=False) \
                .to_csv(path_or_buf=file_name, index=False)
        else:
            concat(result_list).to_csv(path_or_buf=file_name, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='solring 0.0.2')
    parser.add_argument("--url", "-u", required=True, help="The host:port of the running solr.", type=str)
    parser.add_argument("--output", "-o", required=False, default='output', help="Output file name.", type=str)
    parser.add_argument("--save_format", "-sf", required=False, default='txt',
                        help="File type of saved records. Default is txt.",
                        choices=['csv', 'txt'])
    parser.add_argument("--core", "-c", required=True, help="The core/collection in solr.", type=str)
    parser.add_argument("--rows", "-r",
                        required=False,
                        help="The number of row numbers returned. " +
                             "By default, Solr returns 5 batches at a time to save records.",
                        default=5, type=int)
    parser.add_argument("-fl", required=False, default='id',
                        help="Field list to retrieve. By default, Solr returns the id field.", type=str)
    parser.add_argument("-q", required=False, default="*:*",
                        help="Search query. By default, Solr returns all records.", type=str)
    parser.add_argument("-fq", required=False, action='append', help="Filter queries.", type=str)
    parser.add_argument("--score", required=False, action='store_true',
                        help="Learn score of each record in a score field.")
    parser.add_argument("--qt", default='/select', required=False, type=str,
                        help="solr request handle to query on, default is '/select'.")
    subparser_group = parser.add_subparsers(
        title='group command',
        dest='command_group',
        help='group help'
    )
    parser_group = subparser_group.add_parser('group')
    parser_group.add_argument("--group_fl", required=True, action='append',
                              help="The field(s) we want to use to group by.")
    parser_group.add_argument("--group_agg", required=True, action='append',
                              choices=['mean', 'min', 'max', 'count'],
                              help="Aggregation functions to use in group by. Default is count.")
    parser_group.add_argument("--group_column", required=True, action='append',
                              help="The field(s) we want to aggregate.")

    args = parser.parse_args(sys.argv[1:])

    solr_params = {
        'q': args.q,
        'wt': "json",
        'rows': args.rows,
        'score': args.score,
        'fl': args.fl
    }
    group_params = {}
    if args.command_group == 'group':
        group_params = {
            'param_group_by': args.command_group,
            'param_group_fl': args.group_fl,
            'param_group_column': args.group_column,
            'param_group_agg': args.group_agg
        }
    if args.fq:
        solr_params['fq'] = args.fq

    solring = Solring(args.url, args.core, args.qt)
    solring.execute(
        solr_params,
        group_params,
        output=args.output,
        save_format=args.save_format
    )


if __name__ == '__main__':
    main()
