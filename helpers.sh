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

function gh_post_success_comment() {
  #Expects that the GITHUB_AUTH_TOKEN is provided already in the environment
  #Expects that BUILD_URL is provided already in the environment
  # 1st required argument is the repository name like "jstor" or "mylists-service"
  # 2nd required argument is the pull request number
  # 3rd optional argument is the message itself
  REPO="${1:-please-specify-repo}"
  PULL_REQUEST_NUMBER="${2:-please-specify-pr-number}"
  COMMENT_DEFAULT=":white_check_mark: [All Checks Passed](${BUILD_URL})"
  COMMENT_MARKDOWN="${3:-$COMMENT_DEFAULT}"
curl -v -H "Content-Type: application/json" \
 -H "Authorization: token ${GITHUB_AUTH_TOKEN}" \
 -X POST \
 -d "{\"body\":\"${COMMENT_MARKDOWN}\"}" \
  "https://api.github.com/repos/ithaka/${REPO}/issues/${PULL_REQUEST_NUMBER}/comments"
}

function gh_post_failure_comment() {
  #Expects that the GITHUB_AUTH_TOKEN is provided already in the environment
  #Expects that BUILD_URL is provided already in the environment
  # 1st required argument is the repository name like "jstor" or "mylists-service"
  # 2nd required argument is the pull request number
  # 3rd optional argument is the message itself
  REPO="${1:-please-specify-repo}"
  PULL_REQUEST_NUMBER="${2:-please-specify-pr-number}"
  COMMENT_DEFAULT=":x: [Failure](${BUILD_URL})"
  COMMENT_MARKDOWN="${3:-$COMMENT_DEFAULT}"
curl -v -H "Content-Type: application/json" \
 -H "Authorization: token ${GITHUB_AUTH_TOKEN}" \
 -X POST \
 -d "{\"body\":\"${COMMENT_MARKDOWN}\"}" \
  "https://api.github.com/repos/ithaka/${REPO}/issues/${PULL_REQUEST_NUMBER}/comments"
}
