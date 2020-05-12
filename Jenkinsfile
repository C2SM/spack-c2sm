pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                echo "${triggerCause.comment}"
                sh '"${triggerCause.comment}" ./jenkins_build.sh'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
