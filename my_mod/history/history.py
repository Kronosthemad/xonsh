import collections
from xonsh.history.base import History

class CouchDBHistory(History):
    def append(self, cmd):
        self.inps.append(cmd['inp'])
        self.rtns.append(cmd['rtn'])
        self.outs.append(None)
        self.tss.append(cmd.get('ts', (None, None)))
        self._save_to_db(cmd)

        def items(self, newest_first=False):
            yield {'inp': 'couchdb in action', 'ts': 1464652800, 'ind': 0}

        def all_items(self, newest_first=False):
            return self.items()

        def info(self):
            data = collections.OrderedDict()
            data['backend'] = 'couchdb'
            data['sessionid'] = str(self.sessionid)
            return data

        def _save_to_db(self, cmd):
            data = cmd.copy()
            data['inp'] = cmd['inp'].rstrip()
            if 'out' in data:
                data.pop('out')
                data['_id'] = self._build_doc_id()
                try:
                    self._request_db_data('/xonsh-history', data=data)
                except Exception as e:
                    msg = 'failed to save history: {}: {}'.format(e.__class__.__name__, e)
                    print(msg, file=sys.stderr)

        def _build_doc_id(self):
            ts = int(time.time() * 1000)
            return '{}-{}-{}'.format(self.sessionid, ts, str(uuid.uuid4())[:18])

        def _request_db_data(self, path, data=None):
            url = 'http://127.0.0.1:5984' + path
            headers = {'Content-Type': 'application/json'}
            if data is not None:
                resp = requests.post(url, json.dumps(data), headers=headers)
            else:
                headers = {'Content-Type': 'text/plain'}
                resp = requests.get(url, headers=headers)
                return resp




class History:
    def run_gc(self, size=None, blocking=True):
        """Run the garbage collector.

        Parameters
        ----------
        size: None or tuple of a int and a string
            Determines the size and units of what would be allowed to remain.
        blocking: bool
            If set blocking, then wait until gc action finished.
        """
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.gc = None
            self.sessionid = self._build_session_id()
            self.inps = []
            self.rtns = []
            self.outs = []
            self.tss = []

        def _build_session_id(self):
            ts = int(time.time() * 1000)
            return '{}-{}'.format(ts, str(uuid.uuid4())[:18])

        def items(self, newest_first=False):
            yield from self._get_db_items(self.sessionid)

        def all_items(self, newest_first=False):
            yield from self._get_db_items()

        def _get_db_items(self, sessionid=None):
            path = '/xonsh-history/_all_docs?include_docs=true'
            if sessionid is not None:
                path += '&start_key="{0}"&end_key="{0}-z"'.format(sessionid)
                try:
                    r = self._request_db_data(path)
                except Exception as e:
                    msg = 'error when query db: {}: {}'.format(e.__class__.__name__, e)
                    print(msg, file=sys.stderr)
                    return
            data = json.loads(r.text)
                for item in data['rows']:
                    cmd = item['doc'].copy()
                    cmd['ts'] = cmd['ts'][0]
                    yield cmd

