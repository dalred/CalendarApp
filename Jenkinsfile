pipeline {
    agent {
        docker {
            image 'dalred/todoapp:main-version-2793140892'
            args '-p 8081:8081 --network todoapp_mynetwork -e DB_HOST=db -e POSTGRES_PASSWORD=djangoappuserdb -e PORT=5432, -e POSTGRES_USER=djangoappuserdb -e POSTGRES_DB=djangoappuserdb'
        }
    }
    stages {
        stage('git') {
            steps {
                git branch: 'main', url:'https://github.com/dalred/ToDoApp.git'
            }
        }
        stage('tests') {
            steps {
                sh "cd myappcalendar && pytest tests/users/ -vv -k 'not testit'"
            }
        }
    }
    post { // после всей сборки
      cleanup {
          cleanWs()
      }
  }
}

