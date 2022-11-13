pipeline {
    agent any

    environment {
        front_repository = "davidts11/attendance-fronte"
        back_repository = "davidts11/attendance-back"
        registryCredential = 'my-dockerhub-credentials'
      }
      
      
      
    stages {
        
        stage('Checkout') {
            steps {
                echo 'Hello World'
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'my_github', url: 'https://github.com/DAVIDts11/DevOps8200_Final_Project.git']]])
                sh "ls -la"
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                
                // //Cleaning: 
                // sh "docker system prune -f"
                // sh "docker images -q |xargs docker rmi"

                
                //Building images :
                script {
                    dockerImageBack = docker.build(back_repository + ":$BUILD_NUMBER" , "./Back")
                    dockerImageFront = docker.build(front_repository + ":$BUILD_NUMBER" , " ./Front/attendance")
                }
                sh "docker images"
                
                //Pushing docker images to docker hub:
                script {
                     docker.withRegistry( '', registryCredential ) {
                     dockerImageFront.push() 
                     }
                    docker.withRegistry( '', registryCredential ) {
                        dockerImageBack.push() 
                     }
                }
                
            }
        }
        stage('Test') {
            steps {
            //   [ -d ~/.ssh ] || mkdir ~/.ssh && chmod 0700 ~/.ssh
            //         ssh-keyscan -t rsa 172.31.33.36 >> ~/.ssh/known_hosts
            //ssh-keyscan -t rsa test >> ~/.ssh/known_hosts
                echo 'Testing...'
         
            sshagent(['test-deploy-machine-key']) {
                     #echo "TAG=$BUILD_NUMBER" > .env 
                sh "/bin/bash deploy.sh"
                   
            
                        }

             //sh"mkdir -p /Data"
 
             
            }
        }
        stage('Deploy') {
            steps {
           
                echo 'Deploing....'
             //sh "mkdir -p /Data"
   
            }
        }
        
    }
//         post {
//         always {
//         }

//         success {
//         }

//         failure {
//         }
//     }
}
