
pipeline {
    agent any

    environment {
        APP_NAME = "my-python-app"
        DOCKER_REGISTRY = "Docker_Username"   // replace with your Docker Hub username or private registry
        APP_IMAGE = "${DOCKER_REGISTRY}/${APP_NAME}"
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/${APP_NAME}"
        PYTHON = "python3"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
		withPythonEnv('/usr/bin/python3'){
               		sh '''
                  	  whoami
                  	  ${PYTHON} -m venv venv
                   	  . venv/bin/activate
                  	  pip install --upgrade pip
                   	  pip install -r requirements.txt
                    	  pip install flake8 pytest
                	  '''
		}
            }
        }

        stage('Lint') {
            steps {
		withPythonEnv('/usr/bin/python3'){
               	 sh '''
                    . venv/bin/activate
                   # flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
		    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,.venv,.pyenv-usr-bin-python3
                   # flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
                    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics --exclude=venv,.venv,__pycache__,.pyenv-usr-bin-python3

                '''
		}
            }
        }

        stage('Test') {
            steps {
		withPythonEnv('/usr/bin/python3'){
                	sh '''
                    	. venv/bin/activate
	            	export PYTHONPATH=$PYTHONPATH:.
                    	pytest tests/ --disable-warnings --maxfail=3 --junitxml=results.xml
                	'''
		}
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${APP_IMAGE}:${BUILD_NUMBER} ."
            }
        }

        stage('Docker Push') {
           
            steps {
                withCredentials([usernamePassword(credentialsId: 'jenkins-docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        whoami
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:${BUILD_NUMBER}
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                        docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
