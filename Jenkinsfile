pipeline {
    agent none
    stages {
        stage('Run Tests') {
            parallel {
                stage('test on tsa') {
                    agent { label 'tsa' } 
                    steps {
                        sh """
                        module load python/3.7.4
                        srun -c 16 -t 04:00:00 python test_spack.py --tsa """ + env.ghprbCommentBody
                    }
                    steps {
                        def date = sh(returnStdout: true, script: "date -u").trim()
                        def msg = sh(returnStdout: true, script: "cat summary.log").trim()
                        pullRequest.comment("Build ${env.BUILD_ID} ran at ${date}\n${msg}")
                    }
                    post {
                        always {
                            echo 'Cleaning up workspace'
                            deleteDir() 
                        }
                    }
                }
                stage('test on daint') {
                    agent { label 'daint' } 
                    steps {
                        sh """
                        module load cray-python
                        python test_spack.py --daint """ + env.ghprbCommentBody
                    }
                    steps {
                        def date = sh(returnStdout: true, script: "date -u").trim()
                        def msg = sh(returnStdout: true, script: "cat summary.log").trim()
                        pullRequest.comment("Build ${env.BUILD_ID} ran at ${date}\n${msg}")
                    }
                    post {
                        always {
                            echo 'Cleaning up workspace'
                            deleteDir() 
                        }
                    }
                }
            }
        }
    }
}
