pipeline {
    agent none
    stages {
        stage('test on tsa') {
            agent { label 'tsa' } 
            steps {
                sh """
                module load python/3.7.4
                python test_spack.py """ + env.ghprbCommentBody
            }
        }
        stage('test on daint') {
            agent { label 'daint' } 
            steps {
                sh """
                module load cray-python
                python test_spack.py """ + env.ghprbCommentBody
            }
        }
    }
    post {
        always {
            echo 'Cleaning up workspace'
            deleteDir() 
        }
    }
}
