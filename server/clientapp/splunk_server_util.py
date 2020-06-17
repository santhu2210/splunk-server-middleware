from __future__ import print_function
# from __future__ import standard_library
# standard_library.install_aliases()
import urllib.parse, urllib.error, urllib.request
import httplib2
from xml.dom import minidom
import re
import json
from ast import literal_eval


def get_splunk_server_response(serverip, username, passkey, searchquery, earliest_time, latest_time):
    try:
        baseurl = serverip
        userName = username
        password = passkey
        if '|' in searchquery:
            searchqry_lst = searchquery.split('|')
            firs_elm = searchqry_lst[0]+' earliest='+earliest_time+' latest='+latest_time
            remain_elm = '|'.join(searchqry_lst[1:])
            searchQuery = firs_elm +' |'+remain_elm
        else:
            searchQuery = searchquery+' earliest='+earliest_time+' latest='+latest_time


        # searchQuery = 'index="_internal" earliest=06/12/2020:10:00:00 latest=06/15/2020:00:00:00 sourcetype="mongod"'
        # searchQuery = 'index="_internal" earliest=06/12/2020:10:00:00 latest=06/16/2020:00:00:00 | top sourcetype'

        print(" searchQuery :", searchQuery)

        # Authenticate with server.
        # Disable SSL cert validation. Splunk certs are self-signed.
        myhttp = httplib2.Http(disable_ssl_certificate_validation=True)

        # setp 1. Get sessionKey for authenticate
        serverContent = myhttp.request(baseurl + '/services/auth/login', 'POST', headers={}, body=urllib.parse.urlencode({'username':userName, 'password':password}))[1]
        sessionKey = minidom.parseString(serverContent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue

        # Step 2: Create a search job
        # Remove leading and trailing whitespace from the search
        searchQuery = searchQuery.strip()
        # If the query doesn't already start with the 'search' operator or another
        # generating command (e.g. "| inputcsv"), then prepend "search " to it.
        if not (searchQuery.startswith('search') or searchQuery.startswith("|")):
            searchQuery = 'search ' + searchQuery
        print(searchQuery)

        searchjob = myhttp.request(baseurl + '/services/search/jobs', 'POST', headers={'Authorization': 'Splunk %s' % sessionKey}, body=urllib.parse.urlencode({'search': searchQuery}))[1]
        sid = minidom.parseString(searchjob).getElementsByTagName('sid')[0].childNodes[0].nodeValue
        print("====>sid:  %s  <====" % sid)

        # Step 3: Get the search status
        servicessearchstatusstr = '/services/search/jobs/%s/' % sid
        isnotdone = True
        while isnotdone:
            searchstatus = myhttp.request(baseurl + servicessearchstatusstr, 'GET', headers={'Authorization': 'Splunk %s' % sessionKey},)[1]
            isdonestatus = re.compile('isDone">(0|1)')
            print("searchStatus :", type(searchstatus))
            isdonestatus = isdonestatus.search(str(searchstatus)).groups()[0]
            if (isdonestatus == '1'):
                isnotdone = False

        # Step 4: Get the search results
        services_search_results_str = '/services/search/jobs/%s/results?output_mode=json&count=100' % sid
        searchresults_bytes = myhttp.request(baseurl + services_search_results_str, 'GET', headers={'Authorization': 'Splunk %s' % sessionKey},)[1]
        searchresults_string = searchresults_bytes.decode('utf-8')
        searchresults_string = searchresults_string.replace('false', 'False')
        searchresults_dict = literal_eval(searchresults_string)
        searchresults = json.dumps(searchresults_dict, indent=4, sort_keys=True)  # .replace(' ', '&nbsp;').replace('\n', '<br>')
        response_dict = {'searchqry_response': searchresults, 'status': bool(1), 'response_msg': 'Success'}

    except Exception as e:
        print('Exception raised :', str(e))
        response_msg = 'Problem in the server, please check the Ip and credentials'
        response_dict = {'searchqry_response': "", 'status': bool(0), 'response_msg': response_msg}

    return response_dict
