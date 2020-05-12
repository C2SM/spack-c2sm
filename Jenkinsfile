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
