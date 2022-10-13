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
                        """
                    }
                }
            }
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
    triggers {
        extensions {
            commitStatus {
                context('deploy to staging site')
                triggeredStatus('starting deployment to staging site...')
                startedStatus('deploying to staging site...')
                statusUrl('http://mystatussite.com/prs')
                completedStatus('SUCCESS', 'All is well')
                completedStatus('FAILURE', 'Something went wrong. Investigate!')
                completedStatus('PENDING', 'still in progress...')
                completedStatus('ERROR', 'Something went really wrong. Investigate!')
            }
        }
    }
}
