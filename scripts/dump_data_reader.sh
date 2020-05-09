DATA_DIR_DATE=$(date +'%m/%d/%Y')
DATA_PATH="/home/pi/data/${DATA_DIR_DATE}"
FILE_NAME="aircrafts.txt"
echo "$DATA_PATH"
sudo mkdir "$DATA_PATH"
cd $DATA_PATH
touch "$FILE_NAME"
nc 192.168.0.201 30003 >>"$DATA_PATH/$FILE_NAME"
