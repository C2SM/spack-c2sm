import subprocess, re

def get_tags(repo):
    git_obj = subprocess.run(["git", "ls-remote", "--refs", repo],
                             capture_output=True)
    if git_obj.returncode != 0:
        print("\nWarning: no access to {:s} => not fetching versions\n".format(
            repo))
        return []
    return [
        re.match('refs/tags/(.*)', x.decode('utf-8')).group(1)
        for x in git_obj.stdout.split()
        if re.match('refs/tags/(.*)', x.decode('utf-8'))
    ]


def set_versions(repo, regex_filter=None):
    """Detects tags and sets them as versions"""

    def filterfn(repo_tag):
        return re.match(regex_filter, repo_tag) != None

    tags = get_tags(repo)
    if tags:
        if regex_filter:
            tags = list(filter(filterfn, tags))

        for tag in tags:
            version(tag, git=repo, tag=tag, get_full_repo=True)