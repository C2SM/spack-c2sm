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
                            pip install -r requirements.txt
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
                    stage('Bootstrap spack') {
                        steps {
                            sh """
                            source env/bin/activate
                            . ./setup-env.sh
                            spack spec gnuconfig
                            """
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            pytest -v -n auto test/integration_test.py
                            """
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            pytest -v -n auto test/system_test.py
                            """
                        }
                    }
                }
            }
        }
    }
}
