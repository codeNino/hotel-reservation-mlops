pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'melvinai-437118'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Repo to Jenkins.........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/codeNino/hotel-reservation-mlops.git']])
                }
            }
        }

        stage('Building and pushing Docker image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker image to GCR........'
                        sh '''
                        export PATH=$PATH:$(GCLOUD_PATH)

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation-srv:latest .


                        docker push gcr.io/${GCP_PROJECT}/hotel-reservation-srv:latest
                            '''
                }
                }
                
            }
        }


        stage('Deploy to Cloud Run'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker image to GCR........'
                        sh '''
                        export PATH=$PATH:$(GCLOUD_PATH)

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy hotel-reservation-srv \
                            --image=gcr.io/${GCP_PROJECT}/hotel-reservation-srv:latest \
                            --platform=managed \
                            --region africa-south1 \
                             --allow-unauthenticated \
                            --port 8080 \
                             --memory 1024Mi
                       
                }
                }
                
            }
        }
    }
}