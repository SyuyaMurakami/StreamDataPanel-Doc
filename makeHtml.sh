DIR=$(cd $(dirname $0) && pwd)
cd $DIR
sphinx-build -b html ./source ./build/html
sleep 3