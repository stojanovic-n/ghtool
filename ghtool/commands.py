'''
This module contains all commands for consuming GitHub API endpoints.
Commands are basic simple implementation of Command design pattern.
'''
import sys
import requests
import grequests

BASE_GITHUB_API_ENDPOINT = 'https://api.github.com/'
DEFAULT_NUM_OF_REPOS = 10

def exception_handler(request, exception):
    print(exception)
    sys.exit()

class Command:
    '''
    This is base class for implementation of Command
    design pattern with all methods that should be
    overridden in subclasses.
    '''

    def __init__(self, args):
        self.args = args

    def execute(self):
        '''
        This method should have implementation of execution logic
        for specific command.
        '''
        pass

    @staticmethod
    def name():
        '''
        This method should return name of specific command.
        '''
        pass

    @staticmethod
    def add_cmd_subparser(subparsers):
        '''
        This method should add subcommand parser to passed subparsers object.
        '''
        pass


class ListCommand(Command):
    MAP_SORTOPT_TO_PROP = {
        'stars': 'stargazers_count',
        'updated': 'updated_at',
        'forks': 'forks_count'
    }

    def execute(self):
        url = BASE_GITHUB_API_ENDPOINT + 'search/repositories'
        payload = {'per_page': self.args.n, 'page': self.args.page,
                   'order': self.args.order, 'sort': self.args.sort,
                   'q': 'language:' + ' '.join(self.args.language)}
        try:
            res = requests.get(url, params=payload)
        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))
            return

        if res.status_code == 200:
            repos = res.json()['items']
            print('{0:<20} {1:<60} {2}'.format(self.args.sort, 'full_name', 'id'))
            for repo in repos:
                print(
                    '{0:<20} {1:<60} {2}'.format(repo[ListCommand.MAP_SORTOPT_TO_PROP[self.args.sort]],
                                                 repo['full_name'],
                                                 repo['id']))
        elif res.status_code // 100 == 4:
            msgs = [err['message'] for err in res.json()['errors']]
            print('\n'.join(msgs))



    @staticmethod
    def name():
        return 'list'

    @staticmethod
    def add_cmd_subparser(subparsers):
        parser = subparsers.add_parser('list', help='list repositories')
        parser.add_argument('language', help='programming language', nargs='+')
        parser.add_argument('-n', type=int,
                            help='number of repositories per page (DEFAULT: {})'.format(DEFAULT_NUM_OF_REPOS),
                            default=DEFAULT_NUM_OF_REPOS)
        parser.add_argument('-page', type=int,
                            help='page (DEFAULT: 1)',
                            default=1)
        parser.add_argument('-sort', help='sort by field (DEFAULT: \'updated\')', default='updated',
                            choices=list(ListCommand.MAP_SORTOPT_TO_PROP.keys()))
        parser.add_argument('-order', help='sort order (DEFAULT: \'desc\')', default='desc', choices=['desc', 'asc'])


class DescCommand(Command):
    def execute(self):
        url = BASE_GITHUB_API_ENDPOINT + 'repositories/'
        reqs = (grequests.get(url + repo_id) for repo_id in self.args.repo_ids)
        responses = grequests.map(reqs, exception_handler=exception_handler)
        responses = [r for r in responses if r is not None]
        ok_responses = [r for r in responses if r.status_code == 200]
        if len(ok_responses):
            print('{0:10} {1:20} {2:20} {3:20} {4:5} {6:5} {6}'.format('id', 'name', 'owner', 'language', 'stars', 'forks',
                                                                   'html_url'))
            for r in ok_responses:
                item = r.json()
                print('{0:10} {1:20} {2:20} {3:20} {4:5} {5:5} {6}'.format(item['id'], item['name'],
                                                                           item['owner']['login'], item['language'],
                                                                           item['stargazers_count'], item['forks'],
                                                                           item['html_url']))
        else:
            print('No results :(')

    @staticmethod
    def name():
        return 'desc'

    @staticmethod
    def add_cmd_subparser(subparsers):
        parser = subparsers.add_parser('desc', help='description of repositories')
        parser.add_argument('repo_ids', help='Language help', nargs='*')
