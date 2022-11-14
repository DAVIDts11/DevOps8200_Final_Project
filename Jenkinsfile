pipeline {

    agent any
    options { disableConcurrentBuilds() }


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
                
                //Cleaning jenkins machine from dockers : 
                 sh '''if [ $(docker ps -q|wc -l) -gt 0 ] ;
                          then docker ps -q|xargs docker stop ;
                          else  echo  "There is no runnig docker containers on this machine";
                      fi '''
                 sh "docker system prune -af"
                    
                
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
                
                //Configuring .env file :
                sh '''echo "TAG=$BUILD_NUMBER" > .env ;'''
            }
        }
        
        stage('Test') {
            steps {
                //  sh "[ -d ~/.ssh ] || mkdir ~/.ssh && chmod 0700 ~/.ssh "
                //  sh "ssh-keyscan -t rsa test >> ~/.ssh/known_hosts"
                echo 'Testing...'
         
                sshagent(['test-deploy-machine-key']) {
                    sh "/bin/bash deploy.sh test"   
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploing....'
                //  sh "[ -d ~/.ssh ] || mkdir ~/.ssh && chmod 0700 ~/.ssh "
                //  sh "ssh-keyscan -t rsa prod >> ~/.ssh/known_hosts"
                 
                sshagent(['test-deploy-machine-key']) {
                    sh "/bin/bash deploy.sh prod"   
                }
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
