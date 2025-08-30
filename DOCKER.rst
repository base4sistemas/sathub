docker build -t sathub:latest .

v1
docker run --name sathub -p 5000:5000  -v /dev:/dev --privileged  --rm sathub:latest 

v2 - c/ usuário satjub
docker run --name sathub -p 5000:5000  -v /dev/ttyTS0:/dev/ttyTS0 --privileged  --rm sathub:latest

v3
docker run --name sathub -p 5000:5000  --device=/dev/ttyTS0:/dev/ttyTS0 --privileged  --rm sathub:latest

