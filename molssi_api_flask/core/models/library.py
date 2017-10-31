import datetime
from mongoengine import DynamicDocument, StringField, \
                    DateTimeField, BooleanField, ListField


"""
Field Options:
-------------
    db_field: Specify a different field name
    required: Make sure this field is set
    default: Use the given default value if no other value is given
    unique: Make sure no other document in the collection has the same value for this field
    choices: Make sure the field's value is equal to one of the values given in an array
"""


class Library(DynamicDocument):     # or DynamicDocument?
    name = StringField(required=True)
    description = StringField()
    languages = ListField(StringField())
    domain = StringField()          # QM, MM, QM/MM, etc..
    website = StringField()

    published = DateTimeField()
    added = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField()

    # Use the $ prefix to set a text index
    meta = {
        # 'strict': False,  # allow extra fields
        'indexes': [{
                'fields': ['$name', "$description", "domain", "languages"],
                'default_language': "en",
                "language_override": "en",
        }]
    }

    def __str__(self):
        return str(self.id) + ', name: ' + self.name + ', description: ' + \
                self.description + ', languages: ' + str(self.languages) +\
                ', Domain: ' + self.domain
