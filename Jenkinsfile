pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                script {
                    @NonCPS
                    def triggerCause = currentBuild.rawBuild.getCause(org.jenkinsci.plugins.pipeline.github.trigger.IssueCommentCause)
                    echo("${triggerCause.comment}")
                }
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
