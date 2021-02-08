docker build -t sathub:latest .

docker run --name sathub -p 5000:5000  -v /dev:/dev --privileged  --rm sathub:latest 

