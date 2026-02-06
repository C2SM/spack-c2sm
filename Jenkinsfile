pipeline {
    agent none
    environment {
        upstream = '/mch-environment/v8'
    }
    stages {
        stage('Tests') {
            matrix {
                agent { label "${NODENAME}" }
                axes {
                    axis {
                        name 'NODENAME'
                        values 'balfrin'
                    }
                    axis {
                        name 'NTHREADS'
                        values '32'
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
                    stage('System Tests') {
                        steps {
                            sh """
                            source ./setup-env.sh ${upstream}
                            source .venv/bin/activate
                            pytest -v -n  ${NTHREADS} test/common_system_test.py test/balfrin_system_test.py
                            """
                        }
                    }
                }
            }
        }
    }
}
