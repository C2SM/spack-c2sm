pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on daint') {
                    agent { label 'daint' } 
                    steps {
                        sh """
                        sleep 2; 
                        ls; pwd; . ./helpers.sh;
                        gh_post_failure_comment spack-c2sm 469 'test name'
                        """
                    }
                    post {
                        always {
                            echo 'Cleaning up workspace'
                            deleteDir() 
                        }
                    }
                }
            }
        }
    }
}
