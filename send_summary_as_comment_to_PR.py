import glob
import subprocess


class ResultList:

    def __init__(self, artifact_path: str) -> None:
        self.artifact_path = artifact_path
        self.text = ''

    def append(self, status: str, test: str, comment: str = '') -> None:
        self.text += fr'{status} [{test}]({self.artifact_path}/{test}) {comment}\n'


if __name__ == '__main__':
    summary = ResultList(
        'https://jenkins-mch.cscs.ch/job/spack_PR/$BUILD_ID/artifact/')

    # Trigger phrases that cause a test to get a yellow circle
    yellow_triggers = [
        'Timed out waiting for a write lock', 'timed out after 5 seconds'
    ]

    for file_name in glob.glob('*.log'):
        with open(file_name, 'r') as file:
            content = file.read()
            if content.endswith('SUCCESS'):
                summary.append(':green_circle:', file_name)
            else:
                for trigger in yellow_triggers:
                    if trigger in content:
                        summary.append(':yellow_circle:', file_name, trigger)
                        break
                else:
                    summary.append(':red_circle:', file_name)

    if summary.text == '':
        summary.text = 'This message prevents a false negative. Ignore it!'
    # Comment PR
    subprocess.run(
        'curl -v -H "Content-Type: application/json"'\
        ' -H "Authorization: token ${GITHUB_AUTH_TOKEN}"'\
        ' -X POST'\
        ' -d "{\\"body\\":\\"' + summary.text + '\\"}"'\
        ' "https://api.github.com/repos/c2sm/spack-c2sm/issues/${ghprbPullId}/comments"',
        check=True, shell=True)
