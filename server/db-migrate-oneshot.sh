#!/bin/bash

sudo docker exec api "/bin/bash" -c "export FLASK_APP=woojoo && flask db init"
sudo docker exec api "/bin/bash" -c "export FLASK_APP=woojoo && flask db migrate"
sudo docker exec api "/bin/bash" -c "export FLASK_APP=woojoo && flask db upgrade"