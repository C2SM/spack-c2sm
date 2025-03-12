pipeline {
    agent none
    stages {
        stage('Tests') {
            matrix {
                agent { label "${NODENAME}" }
                axes {
                    axis {
                        name 'NODENAME'
                        values 'balfrin'
                    }
                }
                post {
                    always {
                        sh """
                        python3 tools/summarize_logs.py || true
                        """
                        archiveArtifacts artifacts: 'log/*', allowEmptyArchive: true
                        deleteDir()
                    }
                }
                stages {
                    stage('Create python environment') {
                        steps {
                            sh """
                            python3 -m venv .venv
                            source .venv/bin/activate
                            pip install -r requirements.txt
                            """
                        }
                    }
                    stage('Bootstrap spack') {
                        // Bootstrapping spack is a separate stage to avoid problems with concurrently bootstrapping spack in the tests.
                        steps {
                            sh """
                            source ./setup-env.sh
                            spack spec gnuconfig
                            """
                        }
                    }
                    stage('Unit Tests') {
                        steps {
                            sh """
                            source .venv/bin/activate
                            python3 test/unit_test.py
                            """
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh """
                            source ./setup-env.sh /mch-environment/v8
                            source .venv/bin/activate
                            pytest -v -n auto test/integration_test.py
                            """
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh """
                            source ./setup-env.sh /mch-environment/v8
                            source .venv/bin/activate
                            pytest -v -n auto test/common_system_test.py test/balfrin_system_test.py
                            """
                        }
                    }
                }
            }
        }
    }
}
