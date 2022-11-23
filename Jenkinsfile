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
                        archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                        sh "python3 src/report_tests.py --auth_token ${GITHUB_AUTH_TOKEN} --build_id ${BUILD_ID} --issue_id ${ghprbPullId}"
                        deleteDir()
                    }
                }
                stages {
                    stage('Unit Tests') {
                        steps {
                            sh "python3 test/unit_test.py ${NODENAME} > log/${NODENAME}/unit_test/summary.log 2>&1"
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