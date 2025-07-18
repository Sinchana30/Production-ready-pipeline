pipeline {
	agent any
	environment {
		DOCKER_HUB_CREDS = credentials('dockerhub-credentials')
		DOCKER_HUB_USER = 'sinchana30shettar'
		IMG_NAME = ${DOCKER_HUB_USER}/pizza-shop-api
	}
	
	stages {
		stage('Build image') {
			steps{
				echo "Building docker image...."
				
				dir(pizza-shop-api) {
					sh "docker build -t ${IMG_NAME}:${BUILD_NUMBER} ."
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
				echo "Pushing the image to dockerhub...."
				sh "docker push ${IMG_NAME}:${BUILD_NUMBER}" 
				}
		}

		stage('Deploy to Kubernetes') {
			steps{
				echo "Deploying the code to kubernetes...."
				sh """
                		helm upgrade --install pizza-shop ./my-app-chart \
                    		--set image.repository=${IMAGE_NAME} \
                    		--set image.tag=${BUILD_NUMBER} \
                    		--namespace default
                		"""
			}
		}
	
	}
}
		

