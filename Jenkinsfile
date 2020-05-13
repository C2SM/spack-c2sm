pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                script {
                    sh('GITHUB_COMMENT=' + env.GITHUB_COMMENT + './jenkins_build.sh')
                }
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
