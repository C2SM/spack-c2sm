import os
import argparse
import glob
from github import GitHubRepo, Markdown
from machine import machine_name

spack_c2sm_path = os.path.dirname(os.path.realpath(__file__)) + '/..'


class ResultList:

    def __init__(self, artifact_path: str) -> None:
        self.artifact_path = artifact_path
        self.text = ''

    def append(self, status: str, test: str, comment: str = '') -> None:
        link = Markdown.link(test, self.artifact_path + test)
        self.text += f'{status} {link} {comment}\n'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_token', type=str, required=False)
    parser.add_argument('--build_id', type=str, required=False)
    parser.add_argument('--issue_id', type=str, required=True)
    args = parser.parse_args()

    repo = GitHubRepo(group='c2sm',
                      repo='spack-c2sm',
                      auth_token=args.auth_token)
    summary = ResultList(
        f'https://jenkins-mch.cscs.ch/job/Spack/job/spack_PR/{args.build_id}/artifact/log/'
    )

    # Trigger phrases that cause a test to get a yellow circle
    yellow_triggers = [
        'timed out after 5 seconds',
    ]

    for file_name in sorted(glob.glob('log/**/*.log', recursive=True)):
        test_name = file_name.lstrip('log/')
        with open(file_name, 'r') as file:
            content = file.read()
            if content.endswith('OK\n'):
                summary.append(':green_circle:', test_name)
            elif 'AssertionError exception when releasing read lock' in content:
                summary.append(':lock:', test_name, 'spack locking problem')
            elif 'Timed out waiting for a write lock' in content:
                summary.append(':lock:', test_name, 'spack write lock problem')
            elif 'Timed out waiting for a read lock' in content:
                summary.append(':lock:', test_name, 'spack read lock problem')
            elif 'gzip: stdin: decompression OK, trailing garbage ignored' in content:
                summary.append(':wastebasket:', test_name,
                               'spack cached archive problem')
            elif 'DUE TO TIME LIMIT' in content:
                summary.append(':hourglass:', test_name, 'slurm time limit')
            else:
                for trigger in yellow_triggers:
                    if trigger in content:
                        summary.append(':yellow_circle:', test_name, trigger)
                        break
                else:
                    summary.append(':red_circle:', test_name)

    if summary.text == '':
        comment = f'No tests ran on {machine_name()}.'
    else:
        comment = summary.text

    repo.comment(args.issue_id, comment)
