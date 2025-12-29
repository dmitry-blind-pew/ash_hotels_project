
docker network create myNetwork

docker run --name booking_db_container `
    -p 6432:5432 `
    -e  POSTGRES_USER=postgres `
    -e  POSTGRES_PASSWORD=1234 `
    -e  POSTGRES_DB=booking `
    --network=myNetwork `
    --volume ASH-booking-data:/var/lib/postgresql/data `
    -d postgres:16

docker run --name booking_cache_container `
    -p 7379:6379 `
    --network=myNetwork `
    -d redis:7.4

docker run --name booking_nginx_container `
    --volume ./nginx.conf:/etc/nginx/nginx.conf `
    --network=myNetwork `
    -d -p 80:80 nginx


docker build -t booking_image .

docker run --name booking_back
