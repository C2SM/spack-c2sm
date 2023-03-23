import requests


class GitHubRepo:

    def __init__(self, group: str, repo: str, auth_token: str = None) -> None:
        self.group: str = group
        self.repo: str = repo
        self.auth_token: str = auth_token

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
    def table(head, body) -> str:
        data = [head, ['---'] * len(head)] + body
        return '\n'.join(' | '.join(row) for row in data)

    @staticmethod
    def header(text: str, level: int = 1) -> str:
        if (level < 1) or (level > 6):
            raise Exception('Invalid header level')
        return ('#' * level + ' ' + text + '\n')


class HTML:

    @staticmethod
    def link(text: str, url: str) -> str:
        return f'<a href="{url}">{text}</a>'

    @staticmethod
    def table(head, body) -> str:
        table = '<table>'
        table += '<thead>'
        table += '<tr>'
        for cell in head:
            table += f'<th>{cell}</th>'
        table += '</tr>'
        table += '</thead>'
        table += '<tbody>'
        for row in body:
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
