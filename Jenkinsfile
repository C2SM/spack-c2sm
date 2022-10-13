pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on daint') {
                    agent { label 'daint' } 
                    steps {
                        sh """
                        sleep 2
                        """
                    }
                    post {
                        always {
                            sh """
                            source helpers.sh
                            gh_post_failure_comment spack-c2sm 123 'test name'
                            """
                            echo 'Cleaning up workspace'
                            deleteDir() 
                        }
                    }
                }
            }
        }
    }
}
