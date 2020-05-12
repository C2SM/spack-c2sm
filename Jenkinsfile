pipeline {
    agent { label 'tsa' 
    }
    environment { 
        GITHUB_COMMENT = ${env.GITHUB_COMMENT}
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
