from .. import db
from datetime import datetime
import logging
from .software import Software
from flask import request


logger = logging.getLogger(__name__)


class SoftwareAccess(db.Document):
    """Logs searches to a specific software in the DB"""

    software = db.ReferenceField(Software)
    access_date = db.DateTimeField(default=datetime.now)
    ip_address = db.StringField(max_length=100)
    comment = db.StringField(max_length=100)

    meta = {
        'strict': False,                # allow extra fields
        'indexes': [
            "software",
        ]
    }

    def __unicode__(self):
        return self.basis_set_name

    def __str__(self):
        return 'software:' + self.software + ', access_date: ' \
               + self.access_date + ', ip_address: ' + \
                self.ip_address


def save_access(software, comment=None):
    """Save the accessed software, date of access, and IP address
        of the client"""

    ip_address = request.environ.get('REMOTE_ADDR', None)

    log = SoftwareAccess(software=software, ip_address=ip_address,
                         comment=comment)
    log.save()
