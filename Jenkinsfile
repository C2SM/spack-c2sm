script {
    def triggerCause = currentBuild.rawBuild.getCause(org.jenkinsci.plugins.pipeline.github.trigger.IssueCommentCause)
    GITHUB_COMMENT = "${triggerCause.comment}"
}

pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                    sh 'GITHUB_COMMENT=' + GITHUB_COMMENT + ' ./jenkins_build.sh'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
