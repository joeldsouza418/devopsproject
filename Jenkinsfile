pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/joeldsouza418/devopsproject.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop devops-app || true'
                sh 'docker rm devops-app || true'
            }
        }
        stage('Selenium Test') { steps 
            { 
                sh ''' python3 selenium_test.py ''' }
                 
            }

        stage('Run New Container') {
            steps {
                sh 'docker run -d -p 80:8080 --name devops-app devops-app'
            }
        }
    }
}
