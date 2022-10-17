import glob
import subprocess
import os
import sys


def collect_final_status_from_logs():
    failed = []
    write_locked = []
    passed = []

    for log in glob.glob('*.log'):
        with open(log, 'r'):
            if search_str_in_file(log, 'FAIL: SPACK'):
                failed.append(log)
            elif search_str_in_file(log, 'FAIL: TIMEOUT'):
                write_locked.append(log)
            else:
                passed.append(log)

    summary = {}
    summary['failed'] = failed
    summary['write_locked'] = write_locked
    summary['passed'] = passed

    return summary


def search_str_in_file(file_path, word):
    with open(file_path, 'r') as file:
        content = file.read()
        if word in content:
            return True
        else:
            return False


def compose_markdown_comment(machine, status, links):
    comment = '## ' + machine.upper() + ' \\n'

    comment += '  ### Passed \\n'
    for test, link in zip(status['passed'], links['passed']):
        comment = f'{comment} - [{test}]({link}): **PASSED** \\n'

    comment = f'{comment}  ### Failed \\n'
    for test, link in zip(status['failed'], links['failed']):
        comment = f'{comment} - [{test}]({link}): **FAILED** \\n'
    for test, link in zip(status['write_locked'], links['write_locked']):
        comment = f'{comment} - [{test}]({link}): **WRITE LOCK TIMEOUT** \\n'

    return comment


def post_on_PR(comment):
    os.environ['COMMENT_MARKDOWN'] = comment
    command = 'curl -v -H "Content-Type: application/json" '
    command += '-H "Authorization: token ${GITHUB_AUTH_TOKEN}" '
    command += '-X POST '
    command += '-d "{\\"body\\":\\"${COMMENT_MARKDOWN}\\"}" '
    command += '"https://api.github.com/repos/c2sm/spack-c2sm/issues/${ghprbPullId}/comments" '
    subprocess.run(command, check=True, shell=True)


def compose_links_to_artifacts(status):

    base_link = 'https://jenkins-mch.cscs.ch/job/spack_PR'
    pr_id = os.getenv('ghprbPullId')
    pr_link = f'{base_link}/{pr_id}/artifact'

    failed = []
    write_locked = []
    passed = []
    for test in status['passed']:
        passed.append(f'{pr_link}/{test}')

    for test in status['failed']:
        failed.append(f'{pr_link}/{test}')

    for test in status['write_locked']:
        write_locked.append(f'{pr_link}/{test}')

    links = {}
    links['failed'] = failed
    links['write_locked'] = write_locked
    links['passed'] = passed

    return links


if __name__ == '__main__':

    machine = sys.argv[1]

    status = collect_final_status_from_logs()
    links = compose_links_to_artifacts(status)
    comment = compose_markdown_comment(machine, status, links)
    post_on_PR(comment)
