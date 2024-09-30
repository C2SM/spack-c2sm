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
                    stage('Create environment') {
                        steps {
                            sh """
                            python3 -m venv .venv
                            source .venv/bin/activate
                            pip install pytest-xdist
                            """
                        }
                    }
                    stage('Bootstrap spack') {
                        steps {
                            sh """
                            source .venv/bin/activate
                            source ./setup-env.sh
                            spack spec gnuconfig
                            """
                        }
                    }
                    stage('Unit Tests') {
                        steps {
                            sh """
                            source .venv/bin/activate
                            pytest test/unit_test.py
                            """
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh """
                            source .venv/bin/activate
                            source ./setup-env.sh $USER_ENV_ROOT
                            pytest -v -n auto test/integration_test.py
                            """
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh """
                            source .venv/bin/activate
                            source ./setup-env.sh $USER_ENV_ROOT
                            pytest -v -n auto test/system_test.py
                            """
                        }
                    }
                }
            }
        }
    }
}
