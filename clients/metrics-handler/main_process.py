"""
   This is the main processing routine of metrics handler. 
   It will run a metrics query and dump the results.
"""
from .logger import logging, show_msg
import re
import json
import trino

log = logging.getLogger('root')

def main_process(options):
    """
        Main processing routine. Query Trino for three different performance
        metrics and display them to stdout.  
    """
    log.info('User=%s, Host=%s, Port=%s' % (options.user, options.api_host, options.port))
    conn = trino.dbapi.connect(
        host=options.api_host,
        port=options.port,
        user=options.user,
        catalog='jmx'
    )
    cur = conn.cursor()
    # Query JMX for Active Nodes
    cur.execute('SELECT ActiveCount FROM jmx.current."trino.failuredetector:name=HeartbeatFailureDetector"')
    rows = cur.fetchall()
    for row in rows:
       show_msg('ActiveNodes=%s' % row[0])
    # Query JMX for Heap Usage
    cur.execute('SELECT HeapMemoryUsage FROM jmx.current."java.lang:type=Memory"')
    rows = cur.fetchall()
    for row in rows:
       # Heapsize is the first number after "used" in the query output.
       rgx = re.compile('{.*used=(\\d*)}')
       match = rgx.search(row[0])
       if match:
           show_msg('HeapSize=%s' % match.group(1))
    # Query JMX for Active Queries
    cur.execute('SELECT RunningQueries FROM jmx.current."trino.execution:name=QueryManager"')
    rows = cur.fetchall()
    for row in rows:
       show_msg('RunningQueries=%s' % row[0])

