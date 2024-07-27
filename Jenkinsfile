pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'python -m pip install -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'python -m pytest tests/'
      }
    }
    stage('Vulnerability Scan') {
      steps {
        sh 'pip install safety'
        sh 'safety check --full-report'
      }
    }
    stage('Containerize') {
      steps {
        sh 'docker build -t my-fastapi-app .'
        sh 'docker tag my-fastapi-app:latest $DOCKER_HUB_USERNAME/my-fastapi-app:latest'
      }
    }
    stage('Push to Registry') {
      steps {
        sh 'docker push $DOCKER_HUB_USERNAME/my-fastapi-app:latest'
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        kubernetesDeploy(
          configs: 'deployment.yaml',
          enableConfigSubstitution: true
        )
      }
    }
  }
}


environment {
  DOCKER_HUB_USERNAME = 'docker-hub-username'
}