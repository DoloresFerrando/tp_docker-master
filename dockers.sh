
function build_airflow {
  echo "Building Airflow Image"
  cd airflow
  docker build -t airflow/builtin .
  docker images
  cd ..
  echo "Please, check airflow/builtin exists on the docker images list."
}


function build_jupyter {
  echo "Building Jupyterlab Image"
  cd jupyterlab
  docker-compose build
  docker images
  cd ..
  echo "Please, check docker-jupyter-scipy-extensible exists on the docker images list."
}


function init_airflow {
  echo "Upgrading DB and creating user airflow - airflow"
  docker-compose up airflow-init
  docker-compose down --volumes --remove-orphans
  echo "If you read 'docker_airflow-init_1 exited with code 0', then you can exec start_all"
}

function start_all {
  echo "Starting up tpdocker application"
  docker-compose -p tpdocker up -d
}

function info_all {
  echo '
  Everything is ready, access Superset at  http://localhost:/)
  Airlfow at http://localhost:8080/
  Jupyterlab at http://localhost:8888/
  pgAdmin at http://localhost:5050/
  '
}

function stop_all {
  echo "Stopping and removing containers"
  docker-compose -p tpdocker down
}


function start_jupyterl {
  echo "Starting up Jupyter lab"
  cd jupyterlab
  docker-compose -p jupyterl up -d
  docker network connect energy_default jupyterl
  cd ..
}

function info_jupyter {
  echo '
  To access Jupyterlab, please user link with token in logs of container.
  '
}

function stop_jupyter {
  echo "Stopping and removing containers"
  cd jupyterlab
  docker-compose -p jupyterl down
  cd ..
}

function start_airflow {
  echo "Starting Airflow"
  cd airflow
  docker-compose --project-name airflow up -d
  cd ..
}

function info_airflow {
  echo '
  Access Airflow Admin at http://localhost:8080/.
  '
}

function stop_airflow {
  echo "Stopping and removing containers"
  cd airflow
  docker-compose --project-name airflow down
  cd ..
}

function superset-init {
  echo 'Initializing Superset database using sqlite'
  docker exec -it superset superset-init
}

function start_superset {
  echo "Starting Superset"
  cd superset
  docker-compose -p superset up -d
  docker exec -it superset superset init
  cd ..
}

function info_superset {
  echo '
  Access Superset at http://localhost:8088/login/
  User: admin Password: admin
  '
}

function stop_superset {
  echo "Stopping and removing containers"
  cd superset
  docker-compose --p superset down
  cd ..
}

function token {
  echo 'Your TOKEN for Jupyter Notebook is:'
  #SERVER=$(docker exec -it jupyter jupyter notebook list)
  SERVER=$(docker logs jupyter)  
  echo "${SERVER}" | grep 'ServerApp]  or' | sed -E 's/^.*=([a-z0-9]+).*$/\1/'
}

case $1 in
  start_all )
  start_all
  info_all
    ;;

  stop_all )
  stop_all
    ;;

  build_jupyter )
  build_jupyter
    ;;
    
  start_jupyter )
  start_jupyter
  info_jupyter
    ;;

  stop_jupyter )
  stop_jupyter
    ;;

  start_airflow )
  start_airflow
  info_airflow
    ;;

  stop_airflow )
  stop_airflow
    ;;

  init_airflow )
  init_airflow
    ;;

  start_superset )
  start_superset
  info_superset
    ;;

  stop_superset )
  stop_superset
    ;;

  help )
  help
    ;;

  cleanup )
  stop
  cleanup
    ;;

  update )
  update
    ;;

  
  token )
  token
    ;;

  superset-start )
  superset-start
    ;;
  
  superset-stop )
  superset-stop
    ;;

  superset-init )
  superset-init
    ;;

    * )
  printf "ERROR: Missing command\n  Usage: `basename $0` (help|start_all|stop_all|cleanup_all|logs|superset-init)\n"
  exit 1
    ;;
esac
