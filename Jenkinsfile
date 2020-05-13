pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                script {
                    def triggerCause = currentBuild.rawBuild.getCause(org.jenkinsci.plugins.pipeline.github.trigger.IssueCommentCause)
                    sh('GITHUB_COMMENT=' + ${triggerCause.comment} + ' ./jenkins_build.sh')
                }
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
