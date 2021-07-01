if [ -d "web-env" ] 
then
    echo "web-env found" 
else
	echo "web-env not found, creating web-env"
	python3 -m venv web-env
fi
source web-env/bin/activate
pip install -r requirements.txt
export FLASK_APP=mementoweb/validator/web/server.py
flask run
