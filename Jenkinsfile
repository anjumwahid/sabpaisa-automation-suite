pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.49.1-noble'
        }
    }

    environment {
        HEADLESS = 'true'
        SLOW_MO  = '0'
        ENV      = 'staging'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Regression Tests') {
            steps {
                sh 'pytest tests/test_regression_suite.py --alluredir=allure-results -v'
            }
        }
    }

    post {
        always {
            allure results: [[path: 'allure-results']]
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
        }
    }
}
