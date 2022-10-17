import glob
import subprocess
import os


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


def compose_markdown_comment(status):
    comment = '###Passed### \\n'
    for test in status['passed']:
        comment = f'{comment} - {test}: **PASSED** \\n'

    comment = f'{comment} ###Failed### \\n'
    for test in status['failed']:
        comment = f'{comment} - {test}: **FAILED** \\n'

    comment = f'{comment} ###Write lock timeout### \\n'
    for test in status['write_locked']:
        comment = f'{comment} - {test}: **WRITE LOCK TIMEOUT** \\n'

    return comment


def post_on_PR(comment):
    os.environ['COMMENT_MARKDOWN'] = comment
    command = 'curl -v -H "Content-Type: application/json" '
    command += '-H "Authorization: token ${GITHUB_AUTH_TOKEN}" '
    command += '-X POST '
    command += '-d "{\\"body\\":\\"${COMMENT_MARKDOWN}\\"}" '
    command += '"https://api.github.com/repos/c2sm/spack-c2sm/issues/${ghprbPullId}/comments" '
    print(command)
    subprocess.run(command, check=True, shell=True)


if __name__ == '__main__':

    status = collect_final_status_from_logs()
    comment = compose_markdown_comment(status)
    post_on_PR(comment)
