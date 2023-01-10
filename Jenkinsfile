pipeline {
    agent none
    stages {
        stage('Tests') {
            matrix {
                agent { label "${NODENAME}" }
                axes {
                    axis {
                        name 'NODENAME'
                        values 'tsa', 'daint', 'balfrin'
                    }
                }
                post {
                    always {
                        archiveArtifacts artifacts: 'log/**/*.log', allowEmptyArchive: true
                        withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
                            sh """
                            source env/bin/activate
                            python3 src/report_tests.py --auth_token ${GITHUB_AUTH_TOKEN} --build_id ${BUILD_ID} --issue_id ${ghprbPullId}
                            """
                        }
                        deleteDir()
                    }
                }
                stages {
                    stage('Create environment') {
                        steps {
                            sh """
                            python3 -m venv env
                            source env/bin/activate
                            pip install -r requirements.txt
                            """
                        }
                    }
                    stage('Unit Tests') {
                        steps {
                            sh """
                            mkdir -p log/${NODENAME}/unit_test
                            source env/bin/activate
                            python3 test/unit_test.py ${NODENAME} > log/${NODENAME}/unit_test/summary.log 2>&1
                            """
                        }
                    }
                    stage('Bootstrap spack') {
                        steps {
                            sh """
                            source env/bin/activate
                            . ./setup-env.sh
                            spack spec spack
                            """
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            pytest -n auto -q --scope \"""" + env.ghprbCommentBody + "\" test/integration_test.py"
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            pytest -n auto -q --scope \"""" + env.ghprbCommentBody + "\" test/system_test.py"
                        }
                    }
                }
            }
        }
    }
}