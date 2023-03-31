import os
import argparse
import glob
from pathlib import Path
from github import GitHubRepo, Markdown, HTML
from machine import machine_name


class ResultTable:

    def __init__(self, artifact_path: str) -> None:
        self.artifact_path = artifact_path
        self.head = ['', 'Test']
        self.body = []

    def append(self, status: str, log_file: str, comment: str = '') -> None:
        link = HTML.link(Path(log_file).stem, self.artifact_path + log_file)
        self.body.append([status, f'{link} {comment}'])

    def __str__(self) -> str:
        return HTML.table(self.head, self.body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_token', type=str, required=False)
    parser.add_argument('--build_id', type=str, required=False)
    parser.add_argument('--issue_id', type=str, required=True)
    args = parser.parse_args()

    repo = GitHubRepo(group='c2sm',
                      repo='spack-c2sm',
                      auth_token=args.auth_token)
    table = ResultTable(
        f'https://jenkins-mch.cscs.ch/job/Spack/job/spack_PR/{args.build_id}/artifact/'
    )

    # Trigger phrases that cause a test to get a special icon and comment.
    # List[(trigger, icon, comment)]
    triggers = [
        ('AssertionError exception when releasing read lock', ':lock:',
         'spack locking problem'),
        ('Timed out waiting for a write lock', ':lock:',
         'spack write lock problem'),
        ('Timed out waiting for a read lock', ':lock:',
         'spack read lock problem'),
        ('gzip: stdin: decompression OK, trailing garbage ignored',
         ':wastebasket:', 'spack cached archive problem'),
        ('DUE TO TIME LIMIT', ':hourglass:', 'slurm time limit'),
        ('timed out after 5 seconds', ':yellow_circle:',
         'timed out after 5 seconds'),
    ]

    comment = Markdown.header(machine_name(), level=3)
    any_tests_ran_on_machine = False
    for test_type in ['unit', 'integration', 'system']:
        all_tests_of_type_passed = True
        any_tests_of_type = False
        for file_name in sorted(
                glob.glob(f'log/{machine_name()}/{test_type}_test/**/*.log',
                          recursive=True)):
            any_tests_ran_on_machine = True
            any_tests_of_type = True
            with open(file_name, 'r') as file:
                content = file.read()
                if content.endswith('OK\n'):
                    table.append(':green_circle:', file_name)
                else:
                    all_tests_of_type_passed = False
                    for trigger, icon, comment in triggers:
                        if trigger in content:
                            table.append(icon, file_name, comment)
                            break
                    else:
                        table.append(':red_circle:', file_name)

        if any_tests_of_type:
            if all_tests_of_type_passed:
                icon = ':green_circle:'
            else:
                icon = ':red_circle:'
            comment += HTML.collapsible(f'{icon} {test_type} test', table)

        if test_type == 'system' and not os.path.isfile(
                f'log/{machine_name()}/system_test/serial_test_run'):
            comment += '\n\n**WARNING**: Serial tests did not run for system tests'

    if not any_tests_ran_on_machine:
        comment += f'No tests executed.'

    repo.comment(args.issue_id, comment)
