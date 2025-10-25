DIR=$(cd $(dirname $0) && pwd)
cd $DIR
sphinx-autobuild source build/html
sleep 3