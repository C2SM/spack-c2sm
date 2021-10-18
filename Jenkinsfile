pipeline {
    agent none
    stages {
        stage('setup on tsa') {
            agent { label 'tsa' } 
            steps {
                sh """
                module load python/3.7.4
                python ./config.py -m tsa -i . -r ./spack/etc/spack -p ./spack -s ./spack -u OFF -c ./spack-cache
                . spack/share/spack/setup-env.sh
                """
            }
        }
        stage('test on tsa') {
            agent { label 'tsa' } 
            steps {
                sh """
                module load python/3.7.4
                python ./config.py -m tsa -i . -r ./spack/etc/spack -p ./spack -s ./spack -u OFF -c ./spack-cache
                . spack/share/spack/setup-env.sh
                srun -c 14 -t 02:00:00 python3 test_spack.py """ + env.ghprbCommentBody
            }
        }
        stage('setup on daint') {
            agent { label 'daint' } 
            steps {
                sh """
                module load cray-python
                python ./config.py -m daint -i . -r ./spack/etc/spack -p ./spack -s ./spack -u OFF -c ./spack-cache
                . spack/share/spack/setup-env.sh
                """
            }
        }
        stage('test on daint') {
            agent { label 'daint' } 
            steps {
                sh """
                module load cray-python
                python ./config.py -m daint -i . -r ./spack/etc/spack -p ./spack -s ./spack -u OFF -c ./spack-cache
                . spack/share/spack/setup-env.sh
                python3 test_spack.py """ + env.ghprbCommentBody
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
