pipeline {
    agent { label 'tsa' 
    }
    script {
        @NonCPS
        def triggerCause = currentBuild.rawBuild.getCause(org.jenkinsci.plugins.pipeline.github.trigger.IssueCommentCause)
    }
    stages {
        stage('Build') {
            steps {
                echo "${triggerCause.comment}"
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
