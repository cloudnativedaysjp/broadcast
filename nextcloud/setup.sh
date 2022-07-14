# docker-compose exec -u www-data app bash

apt install python python3 python3-pip jq -y
pip install nextcloud-api-wrapper
docker-compose up -d

while :
do
  curl localhost > /dev/null 2>&1
  if [ "${?}" -eq 0 ]; then
    echo server is running!
    break
  else
    echo server is starting...
  fi
  sleep 2
done

docker-compose exec -u www-data app ./occ app:disable dashboard
docker-compose exec -u www-data app ./occ app:install groupfolders

docker-compose exec -u www-data app ./occ group:add general

echo "## type kameneko password"
docker-compose exec -u www-data app ./occ user:add kameneko --group=general --group=admin
docker-compose exec -u www-data app ./occ groupfolders:create general

general_folder_id = $(docker-compose exec -u www-data app ./occ groupfolders:list --output json | jq -r '.[].id')
docker-compose exec -u www-data app ./occ groupfolders:group ${general_folder_id} general write
docker-compose exec -u www-data app ./occ groupfolders:group ${general_folder_id} general share

docker-compose exec -u www-data app ./occ groupfolders:scan ${general_folder_id}

export NEXTCLOUD_HOSTNAME="uploader.cloudnativedays.jp"
export NEXTCLOUD_ADMIN_USER="kamenekeo"
# export NEXTCLOUD_ADMIN_PASSWORD="your_nextcloud_password"
read -sp "type kemeneko password: " NEXTCLOUD_ADMIN_PASSWORD