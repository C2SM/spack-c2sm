pipeline {
    agent { label 'tsa' }
    
    stages {
        stage('setup') {
            steps {
                sh """
                module load python/3.7.4
                python ./config.py -m tsa -i . -r ./spack/etc/spack -p $PWD/spack -s $PWD/spack -u OFF -c ./spack-cache
                source ./spack/share/spack/setup-env.sh
                """
            }
        }
        stage('test') {
            steps {
                sh """
                srun -c 14 -t 02:00:00 python test_spack.py
                """
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
