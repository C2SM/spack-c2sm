pipeline {
    agent any

    stages {
        stage('Install Spack Instance') {
            steps {
                echo 'Install spack temp instance with branch config files and mch spack packages'
                sh './config.py -m $slave -i . -r ./spack/etc/spack -p $PWD/spack -u OFF'
                echo 'Source spack instance'
                sh '. spack/share/spack/setup-env.sh'
            }
        }
        stage('Install spec') {
            steps {
                echo 'spack install ${GITHUB_COMMENT#"launch jenkins "}'
                sh 'spack install ${GITHUB_COMMENT#"launch jenkins "}'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
