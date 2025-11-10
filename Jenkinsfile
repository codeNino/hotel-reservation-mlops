pipeline {
    agent any

    environment {
    VENV_DIR = 'venv'
    GCP_PROJECT = 'melvinai-437118'
    GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    UV_PATH = '/var/jenkins_home/.local/bin'
    KUBECTL_AUTH_PLUGIN = '/usr/lib/google-cloud-sdk/bin'
    PATH = "${UV_PATH}:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}:/usr/local/bin:/usr/bin:/bin"
}


    stages {

        stage('Verify tools') {
            steps {
        sh '''
        echo "PATH is: $PATH"
        which uv || echo "uv not found"
        which gcloud || echo "gcloud not found"
        which kubectl || echo "kubectl not found"
        '''
    }
}


        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Repo to Jenkins.........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/codeNino/hotel-reservation-mlops.git']])
                }
            }
        }

        stage("Making virtual environment..."){
            steps{
                script{
                    echo 'Making a virtual environment'
                    sh '''
                        which uv
                        uv --version
                        uv venv ${VENV_DIR}
                        uv add dvc
                    '''
                }
            }
        }

        stage("DVC Pull"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Pulling Artifacts with DVC....'
                        sh '''
                        uv run dvc pull
                        '''
                    }
                }
            }
        }

        stage('Building and pushing Docker image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker image to GCR........'
                        sh '''

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        export DOCKER_BUILDKIT=1

                        docker buildx build --platform linux/amd64 -t gcr.io/${GCP_PROJECT}/hotel-reservation-srv:latest .

                        docker push gcr.io/${GCP_PROJECT}/hotel-reservation-srv:latest
                            '''
                }
                }
                
            }
        }


        stage('Deploy to Kubernetes'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker image to GCR........'
                        sh '''
                        export PATH=$PATH:$(GCLOUD_PATH)

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud container clusters get-credentials mlops-nino-cluster --region us-east1

                        kubectl apply -f deployment.yaml
                        '''

                        
                       
                }
                }
                
            }
        }
    }
}