pipeline {
  agent any

  environment {
    PROJECT_ID = "YOUR_GCP_PROJECT_ID"
    REGION = "asia-south1"
    SERVICE_NAME = "devops-demo-app"
    REPO = "devops-demo-repo" // artifact repo name
    IMAGE = "asia-south1-docker.pkg.dev/${env.PROJECT_ID}/${env.REPO}/${env.SERVICE_NAME}:$BUILD_NUMBER"
    GCP_CREDENTIALS_ID = "gcp-service-account-json" // set this in Jenkins credentials
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker') {
      steps {
        withCredentials([file(credentialsId: env.GCP_CREDENTIALS_ID, variable: 'GCP_KEY')]) {
          sh '''
            # Authenticate gcloud for access to Artifact Registry (used later)
            gcloud auth activate-service-account --key-file=$GCP_KEY
            gcloud config set project $PROJECT_ID

            # Build docker image
            docker build -t $IMAGE .
          '''
        }
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([file(credentialsId: env.GCP_CREDENTIALS_ID, variable: 'GCP_KEY')]) {
          sh '''
            gcloud auth activate-service-account --key-file=$GCP_KEY
            gcloud config set project $PROJECT_ID

            # Allow Docker to push to Artifact Registry
            gcloud auth configure-docker asia-south1-docker.pkg.dev -q

            docker push $IMAGE
          '''
        }
      }
    }

    stage('Deploy to Cloud Run') {
      steps {
        withCredentials([file(credentialsId: env.GCP_CREDENTIALS_ID, variable: 'GCP_KEY')]) {
          sh '''
            gcloud auth activate-service-account --key-file=$GCP_KEY
            gcloud config set project $PROJECT_ID

            gcloud run deploy $SERVICE_NAME \
              --image=$IMAGE \
              --region=$REGION \
              --platform=managed \
              --allow-unauthenticated \
              --quiet
          '''
        }
      }
    }
  }
}
