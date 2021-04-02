set -x
echo $1
id=$(docker run -d -p 2222:22 sshmock ) 
echo $id
sleep $1
docker stop $id
docker rm $id
