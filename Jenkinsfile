pipeline {
    agent any

    environment {
        HEADLESS = 'true'
        SLOW_MO  = '0'
        ENV      = 'staging'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
                bat 'playwright install chromium'
            }
        }

        stage('Run Regression Tests') {
            steps {
                bat 'pytest tests/test_regression_suite.py --alluredir=allure-results -v'
            }
        }
    }

    post {
        always {
            allure results: [[path: 'allure-results']]
        }
    }
}
