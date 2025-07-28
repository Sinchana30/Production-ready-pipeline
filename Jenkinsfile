// Jenkinsfile - DEBUGGING VERSION

pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDS = credentials('dockerhub-credentials')
        DOCKER_HUB_USER  = 'your-dockerhub-username' // Make sure this is correct!
        
        // We are using the PATH override method. Let's see what 'tool' returns.
        // A common issue is that the tool home is not /usr/bin but just /usr, so let's try that.
        PATH = "${tool 'docker-host'}:${env.PATH}"
    }

    stages {
        
        // VVVVV THIS IS THE NEW DEBUGGING STAGE VVVVV
        stage('Debug Environment') {
            steps {
                echo "--- STARTING ENVIRONMENT DEBUG ---"
                
                // Question 1: What is the full PATH variable?
                sh 'echo "Current PATH is: $PATH"'
                
                // Question 2: Can you find the 'docker' command anywhere?
                // The '|| true' part ensures the build doesn't fail if 'which' returns an error.
                sh 'which docker || true'
                
                // Question 3: What is inside /usr/bin? Let's look for docker there.
                sh 'ls -l /usr/bin/docker || true'

                // Bonus Question: What about just /usr?
                sh 'ls -l /usr/docker || true'

                echo "--- FINISHED ENVIRONMENT DEBUG ---"
            }
        }
        // ^^^^^ THIS IS THE NEW DEBUGGING STAGE ^^^^^


        stage('Build Docker Image') {
            // ... this stage and the others remain the same
            steps {
                script {
                    def IMAGE_NAME = "${env.DOCKER_HUB_USER}/pizza-shop-api"
                    echo "Building the Docker image: ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                    dir('pizza-shop-api') {
                        sh "docker build -t ${IMAGE_NAME}:${env.BUILD_NUMBER} ."
                    }
                }
            }
        }
        // ... all your other stages

	stage('Docker Login') {
                        steps {
                                echo "logging into dockerhub...."

                                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_HUB_CREDS_PWD', usernameVariable: 'DOCKER_HUB_CREDS_USER')]) {
                                        sh "echo $DOCKER_HUB_CREDS_PWD | docker login -u $DOCKER_HUB_CREDS_USER --password-stdin"
                                        }
                                }
                }

                stage('Push to DockerHub') {
                        steps{
                                script{
                                echo "Pushing the image to dockerhub...."
                                def IMG_NAME = "${env.DOCKER_HUB_USER}/pizza-shop-api"
                                sh "docker push ${IMG_NAME}:${env.BUILD_NUMBER}"
                                }
                        }
                }

                stage('Deploy to Kubernetes') {
                        steps{
                                script{
                                def IMG_NAME = "${env.DOCKER_HUB_USER}/pizza-shop-api"
                                echo "Deploying the code to kubernetes...."
                                sh """
                                helm upgrade --install pizza-shop ./my-app-chart \
                                --set image.repository=${IMG_NAME} \
                                --set image.tag=${env.BUILD_NUMBER} \
                                --namespace default
                                """
                                }
                        }
                }

    }
}
