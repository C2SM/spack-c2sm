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
                        deleteDir()
                    }
                }
                stages {
                    stage('Unit Tests') {
                        steps {
                            sh "test/test_env_setup_machine.sh ${NODENAME} >> ${NODENAME}_unit_test.log 2>&1"
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh "python3 test/integration_test.py >> ${NODENAME}_integration_test.log 2>&1"
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh "python3 test/system_test.py >> ${NODENAME}_system_test.log 2>&1"
                        }
                    }
                }
            }
        }
    }
}