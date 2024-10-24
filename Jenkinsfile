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
                            python3 -m venv env
                            source env/bin/activate
                            pip install pytest-xdist
                            """
                        }
                    }
                    stage('Bootstrap spack') {
                        // Bootstrapping spack is a separate stage to avoid problems with concurrently bootstrapping spack in the tests.
                        steps {
                            sh """
                            source env/bin/activate
                            source ./setup-env.sh
                            spack spec gnuconfig
                            """
                        }
                    }
                    stage('Unit Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            python3 test/unit_test.py
                            """
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            source ./setup-env.sh $USER_ENV_ROOT
                            pytest -v -n auto test/integration_test.py
                            """
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh """
                            source env/bin/activate
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
