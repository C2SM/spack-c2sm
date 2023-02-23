import requests


class GitHubRepo:

    def __init__(self, group: str, repo: str, auth_token: str = None) -> None:
        self.group: str = group
        self.repo: str = repo
        self.auth_token: str = auth_token

    def get_test_result(test, logfiles, col):
        test_exist = False
        test_col = ':green_circle:'
        for c, logfile in zip(col, logfiles):
            if test in logfile:
                test_exist = True
                if c == ':red_circle:' or c == ':lock:' or c == ':wastebasket:' or c == ':hourglass:':
                    test_col = ':red_circle:'
                elif c == ':yellow_circle:' and not test_col == ':red_circle:':
                    test_col = ':yellow_circle:'
        return (test_exist, test_col)

    def add_test_to_text(test, test_exist, test_col, col, logfiles, text):
        if test_exist:
            details = [['', 'Test']]
            for i in range(len(logfiles)):
                if test in logfiles[i]:
                    details.append([col[i], logfiles[i]])
            text = text + HTML.collapsible(test_col + ' ' + test + ' test',
                                           HTML.table(details))
        return (text)

    def comment(self, issue_id: str, text: str) -> None:
        url = f'https://api.github.com/repos/{self.group}/{self.repo}/issues/{issue_id}/comments'

        headers = {'Content-Type': 'application/json'}
        if self.auth_token is not None:
            headers['Authorization'] = 'token ' + self.auth_token

        requests.post(url, headers=headers, json={'body': text})


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


class HTML:

    @staticmethod
    def link(text: str, url: str) -> str:
        return f'<a href="{url}">{text}</a>'

    @staticmethod
    def table(data) -> str:
        table = '<table>'
        table += '<thead>'
        table += '<tr>'
        for cell in data[0]:
            table += f'<th>{cell}</th>'
        table += '</tr>'
        table += '</thead>'
        table += '<tbody>'
        for row in data[1:]:
            table += '<tr>'
            for cell in row:
                table += f'<td>{cell}</td>'
            table += '</tr>'
        table += '</tbody>'
        table += '</table>'
        return table

    @staticmethod
    def collapsible(summary: str, details: str) -> str:
        return f'<details><summary>{summary}</summary>{details}</details>'
