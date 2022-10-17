pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on tsa') {
                    agent { label 'tsa' } 
                    steps {
                        sh """
                        module load python/3.7.4
                        python test_spack.py --tsa """ + env.ghprbCommentBody
                    }
                    post {
                        always {
                            withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
                                sh"""
                                module load cray-python
                                python send_summary_as_comment_to_PR.py  'tsa'
                                """
                            }
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
                        module load cray-python
                        python test_spack.py --daint """ + env.ghprbCommentBody
                    }
                    post {
                        always {
                            withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
                                sh"""
                                module load cray-python
                                python send_summary_as_comment_to_PR.py  'daint'
                                """
                            }
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
