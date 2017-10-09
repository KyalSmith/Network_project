#!/bin/bash

git clone https://github.com/phoemur/ipgetter.git
unzip ipgetter.zip
cd ipgetter/
python3 setup.py install

cd ../
git clone https://github.com/pyqtgraph/pyqtgraph.git
unzip pyqtgraph.zip
cd pyqtgraph/
python3 setup.py install
