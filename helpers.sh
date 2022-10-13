#!/bin/bash

#Jenkins provides:
#GIT_COMMIT like ce9a3c1404e8c91be604088670e93434c4253f03
#GIT_BRANCH like origin/master
#BUILD_URL like http://jenkins.test.cirrostratus.org/job/Article_View_c20n_Full_Non_Destructive_Full_Suite/1334/

# per https://wiki.jenkins-ci.org/display/JENKINS/GitHub+pull+request+builder+plugin
# The jenkins pull request builder plugin (if configured) will provide these:
#ghprbPullId
#ghprbActualCommit
#ghprbActualCommitAuthor
#ghprbActualCommitAuthorEmail
#ghprbPullDescription
#ghprbPullId
#ghprbPullLink
#ghprbPullTitle
#ghprbSourceBranch
#ghprbTargetBranch
#sha1

#Run these functions like this:
# BUILD_URL="";gh_post_success_comment "mylists-service" "48"
function gh_post_comment() {
  PULL_REQUEST_NUMBER=$1
  COMMENT_MARKDOWN=$2
curl -v -H "Content-Type: application/json" \
 -H "Authorization: token ${GITHUB_AUTH_TOKEN}" \
 -X POST \
 -d "{\"body\":\"${COMMENT_MARKDOWN}\"}" \
  "https://api.github.com/repos/c2sm/spack-c2sm/issues/${PULL_REQUEST_NUMBER}/comments"
}
