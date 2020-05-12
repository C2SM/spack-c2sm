pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                sh './jenkins_build.sh'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
