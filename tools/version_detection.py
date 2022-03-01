import subprocess, re
from spack import *


def get_tags(repo):
    git_obj = subprocess.run(["git", "ls-remote", "--refs", repo],
                             capture_output=True)
    if git_obj.returncode != 0:
        return []
    else:
        git_tags = [
            re.match('refs/tags/(.*)', x.decode('utf-8')).group(1)
            for x in git_obj.stdout.split()
            if re.match('refs/tags/(.*)', x.decode('utf-8'))
        ]
        return git_tags


def set_versions(version, repo, tag_prefix=None, regex_filter=None):
    """Detects tags in 'repo' that match the 'regex_filter' and adds them as versions prefixed with 'tag_prefix'."""

    def filterfn(repo_tag):
        return re.match(regex_filter, repo_tag) != None

    tags = get_tags(repo)
    if tags:
        if regex_filter:
            tags = list(filter(filterfn, tags))

        for tag in tags:
            version(tag_prefix + '_' + tag if tag_prefix else tag,
                    git=repo,
                    tag=tag,
                    get_full_repo=True)
