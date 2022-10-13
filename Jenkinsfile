pipeline {
    withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
        agent none
        stages {
            stage('Run Tests') {
                parallel {
                    stage('test on daint') {
                        agent { label 'daint' } 
                            steps {
                                sh """
                                . ./helpers; gh_post_failure_comment 'spack-c2sm' 557 'test_messgfa'
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
}
