pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on daint') {
                    agent { label 'daint' } 
                    steps {
                        sh """
                        module load cray-python
                        """
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                            echo 'Cleaning up workspace'
                            deleteDir() 
                        }
                    }
                }
            }
        }
    }
}
