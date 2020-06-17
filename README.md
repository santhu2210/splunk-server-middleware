# splunk-server-middleware
The splunk server's logs searcher and sender application, It's mainly developed by using django, python, java-script, bootstrap.


### prerequisite packages:
1. python3
2. pip3 (as default pip)

## Configuration and setup:
### local system deployment (run below commands in present location)
1.  Create python3 virtual environment `virtualenv -p python3 <envr-name>`
2.  Activate the environment  `source <envr-name>/bin/activate`
3.  Install requirements packages `pip install -r requirements.txt`.
4.  Run django server by using bash script `bash server/run_devel_server.sh`
5.  Server wil run on 8000 port in localhost
