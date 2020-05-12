pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                sh '${env.GITHUB_COMMENT} ./jenkins_build.sh'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
