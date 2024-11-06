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
                            python3 -m venv env
                            source env/bin/activate
                            pip install -r requirements.txt
                            """
                        }
                    }
                    stage('Create uenv') {
                        steps {
                            sh """
                            git clone -b fix/jenkins https://github.com/eth-cscs/uenv.git
                            ./uenv/install --yes --destdir=$WORKSPACE
                            source $WORKSPACE/etc/profile.d/uenv.sh
                            uenv repo create
                            uenv image pull mch/v8:rc1
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
                            source $WORKSPACE/etc/profile.d/uenv.sh
                            uenv start mch/v8:rc1
                            source ./setup-env.sh /user-environment
                            pytest -v -n auto test/integration_test.py
                            """
                        }
                    }
                    stage('System Tests') {
                        steps {
                            sh """
                            source env/bin/activate
                            source $WORKSPACE/etc/profile.d/uenv.sh
                            uenv start mch/v8:rc1
                            source ./setup-env.sh /user-environment
                            pytest -v -n auto test/system_test.py
                            """
                        }
                    }
                }
            }
        }
    }
}
