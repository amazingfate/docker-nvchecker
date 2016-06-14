echo "deb http://pools.corp.deepin.com/deepin/ unstable main contrib non-free" > /etc/apt/sources.list
apt-get update
apt-get install -y python3-apt python3-pip python3-setuptools git
pip3 install nvchecker
cd /nvchecker
touch .nvchecker.old.txt
nvchecker nvchecker.ini > nv.log 2>&1
echo "================================================================================"
python3 log2json_nv.py nv.log
