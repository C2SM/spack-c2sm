import requests


class GitHubRepo:

    def __init__(self, group: str, repo: str, auth_token: str = None) -> None:
        self.group: str = group
        self.repo: str = repo
        self.auth_token: str = auth_token

    def get_color(test, details, col):
        test_exist = False
        test_col = ':green_circle:'
        for i in range(len(details)):
            if test in details[i][1]:
                test_exist = True
                if col[i] == ':red_circle:' or col[i] == ':lock:' or col[
                        i] == ':wastebasket:' or col[i] == ':hourglass:':
                    test_col = ':red_circle:'
                elif col[
                        i] == ':yellow_circle:' and not test_col == ':red_circle:':
                    test_col = ':yellow_circle:'
        return (test_exist, test_col)

    def add_test_to_text(test, test_exist, test_col, details, col, text):
        if test_exist:
            text = text + '<details>\n<summary>' + test_col + ' ' + test + ' test</summary>\n<table>\n<tbody>\n'
            for i in range(len(details)):
                if test in details[i][1]:
                    test_name = details[i][2].replace('_', ' ')
                    test_name = test_name.replace('.log', '')
                    text = text + '<tr><td>' + col[i]
                    text = text + '</td><td>' + test_name + '</td></tr>\n'
            text = text + '</tbody>\n</table>\n</details>'
        return (text)

    def comment(self, issue_id: str, text: str) -> None:
        url = f'https://api.github.com/repos/{self.group}/{self.repo}/issues/{issue_id}/comments'

        headers = {'Content-Type': 'application/json'}
        if self.auth_token is not None:
            headers['Authorization'] = 'token ' + self.auth_token

        f = filter(None, text.split('\n'))
        text_lines = list(f)

        details = []
        col = []
        for item in text_lines:
            details.append(item[item.find('[') + 1:item.rfind(']')])
            col.append(item.split()[0])

        for i, item in enumerate(details):
            details[i] = item.split('/')

        text_new = '### ' + details[0][0] + '\n'

        [unit, unit_col] = GitHubRepo.get_color('unit', details, col)
        text_new = GitHubRepo.add_test_to_text('unit', unit, unit_col, details,
                                               col, text_new)
        [int, int_col] = GitHubRepo.get_color('integration', details, col)
        text_new = GitHubRepo.add_test_to_text('integration', int, int_col,
                                               details, col, text_new)
        [sys, sys_col] = GitHubRepo.get_color('system', details, col)
        text_new = GitHubRepo.add_test_to_text('system', sys, sys_col, details,
                                               col, text_new)

        requests.post(url, headers=headers, json={'body': text_new})


class Markdown:
    # Source: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

    @staticmethod
    def ordered_list(elements: list) -> str:
        return '\n'.join(f'{i+1}. {e}' for i, e in enumerate(elements))

    @staticmethod
    def unordered_list(elements: list) -> str:
        return '\n'.join(f'* {e}' for e in elements)

    @staticmethod
    def link(text: str, url: str) -> str:
        return f'[{text}]({url})'

    @staticmethod
    def image(alt_text: str, url: str) -> str:
        return f'![{alt_text}]({url})'

    @staticmethod
    def inline_code(code: str) -> str:
        return f'`{code}`'

    @staticmethod
    def code(code: str, language: str = '') -> str:
        return f'```{language}\n{code}\n```'

    @staticmethod
    def table(data) -> str:
        return '\n'.join(
            ' | '.join(str(cell) for cell in row)
            for row in [data[0], ['---' for d in data[0]], *data[1:]])

    @staticmethod
    def collapsible(summary: str, details: str) -> str:
        return f'<details><summary>{summary}</summary>{details}</details>'
