 @NonCPS
 def triggerCause = currentBuild.rawBuild.getCause(org.jenkinsci.plugins.pipeline.github.trigger.IssueCommentCause)

pipeline {
    agent { label 'tsa' 
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
