pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                echo "${env.GITHUB_COMMENT}"
                sh '"${env.GITHUB_COMMENT}" ./jenkins_build.sh'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
