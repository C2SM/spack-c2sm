
import subprocess, re
from spack import *

def get_releases(repo):
    git_obj = subprocess.run(["git", "ls-remote", "--refs", repo],
                             capture_output=True)
    if git_obj.returncode != 0:
        print("\nWarning: no access to {:s} => not fetching versions\n".format(
            repo))
        return []
    else:
        git_tags = [
            re.match('refs/tags/(.*)', x.decode('utf-8')).group(1)
            for x in git_obj.stdout.split()
            if re.match('refs/tags/(.*)', x.decode('utf-8'))
        ]
        return git_tags


def set_versions(repo, reg_filter=None):
    def filterfn(repo_tag):
        return re.match(reg_filter, repo_tag) != None

    tags = get_releases(repo)
    if tags:
        if reg_filter:
            tags = list(filter(filterfn, tags))

        for tag in tags:
            version(tag, git=repo, tag=tag, get_full_repo=True)

