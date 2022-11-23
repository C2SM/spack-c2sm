pipeline {
    agent none
    stages {
        stage('Tests') {
            matrix {
                agent { label "${NODENAME}" }
                axes {
                    axis {
                        name 'NODENAME'
                        values 'tsa', 'daint', 'dom', 'manali', 'balfrin'
                    }
                }
                post {
                    always {
                        archiveArtifacts artifacts: 'log/**/*.log', allowEmptyArchive: true
                        withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
                            sh """
                            load_python.sh ${NODENAME}
                            python3 src/report_tests.py --auth_token ${GITHUB_AUTH_TOKEN} --build_id ${BUILD_ID} --issue_id ${ghprbPullId}
                            """
                        }
                        deleteDir()
                    }
                }
                stages {
                    stage('Unit Tests') {
                        steps {
                            sh """
                            mkdir -p log/${NODENAME}/unit_test
                            load_python.sh ${NODENAME}
                            python3 test/unit_test.py ${NODENAME} > log/${NODENAME}/unit_test/summary.log 2>&1
                            """
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh "python3 test/integration_test.py"
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh "python3 test/system_test.py"
                        }
                    }
                }
            }
        }
    }
}