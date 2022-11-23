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
    def table(data) -> str:
        return '\n'.join(
            ' | '.join(str(cell) for cell in row)
            for row in [data[0], ['---' for d in data[0]], *data[1:]])

    @staticmethod
    def collapsible(summary: str, details: str) -> str:
        return f'<details><summary>{summary}</summary>{details}</details>'
