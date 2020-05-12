pipeline {
    agent { label 'tsa' 
    }
    stages {
        stage('Build') {
            steps {
                echo 'Install spack temp instance with branch config files and mch spack packages'
                sh './config.py -m tsa -i . -r ./spack/etc/spack -p $PWD/spack -u OFF'
                echo 'Source spack instance'
                sh '. spack/share/spack/setup-env.sh'
                echo 'spack install ${GITHUB_COMMENT#"launch jenkins "}'
                sh 'spack install ${GITHUB_COMMENT#"launch jenkins "}'
            }
        }
    }
    
    triggers {
        issueCommentTrigger('launch jenkins.*')
    }
}
