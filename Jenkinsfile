pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on tsa') {
                    agent { label 'tsa' } 
                    steps {
                        sh """
                        source setup-env.sh
                        python test_spack.py --tsa """ + env.ghprbCommentBody
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                            echo 'Cleaning up workspace'
                            deleteDir() 
                        }
                    }
                }
                stage('test on daint') {
                    agent { label 'daint' } 
                    steps {
                        sh """
                        source setup-env.sh
                        python test_spack.py --daint """ + env.ghprbCommentBody
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
