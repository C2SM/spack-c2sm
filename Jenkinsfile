pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on daint') {
                    agent { label 'daint' } 
                        steps {
                            withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
                                sh """
                                . ./helpers.sh; gh_post_failure_comment 'spack-c2sm' 557 'first list \n second line \n third line'
                                """
                            }
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
