pipeline {
	agent any
	tools {
	dockerTool 'docker-host'
	}
	environment {
		DOCKER_HUB_CREDS = credentials('dockerhub-credentials')
		DOCKER_HUB_USER = 'sinchana30shettar'
		}
	
	stages {
		stage('Build image') {
			steps{
				script{
				echo "Building docker image...."
				
				def IMG_NAME = "${env.DOCKER_HUB_USER}/pizza-shop-api"
				dir('pizza-shop-api') {
					sh "docker build -t ${IMG_NAME}:${env.BUILD_NUMBER} ."
					}	
				}
			}
		}
	
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
		

