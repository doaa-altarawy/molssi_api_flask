import datetime
from flask_mongoengine.wtf import model_form
from .. import db


"""
Fields: http://docs.mongoengine.org/apireference.html
mongoengine.fields.

Field Options:
-------------
    db_field: Specify a different field name
    required: Make sure this field is set
    default: Use the given default value if no other value is given
    unique: Make sure no other document in the collection has the same value for this field
    choices: Make sure the field's value is equal to one of the values given in an array
"""


class QMFeatures(db.EmbeddedDocument):
    """QM specific features"""

    basis = db.StringField(max_length=200)
    element_coverage = db.StringField(max_length=200)
    other = db.StringField(max_length=250)

    # tags
    TAG_NAMES = [
                "semiempirical",  # fff
                "dft",
                "dft_u",
                "hybrid",
                "rohf",
                "uhf",
                "mcscf",
                "ci",
                "mp_or_mbpt",
                "cc",
                "rpa",
                "gf",
                "tddft",
                "dmf",
                "fequencies_phonons",
                "nmr",
                "symmetry"
    ]

    tags = db.ListField(db.StringField(max_length=20, choices=TAG_NAMES))

    def add_tags(self, kwargs):
        self.tags = []
        for tag in self.TAG_NAMES:
            if tag in kwargs:
                tag_val = kwargs.pop(tag, '')
                if tag_val and tag_val.lower() not in ['', 'no', 'false']:
                    self.tags.append(tag)


class MMFeatures(db.EmbeddedDocument):
    """MM specific features"""

    ensembles = db.StringField(max_length=200)
    free_energy_methods = db.StringField(max_length=200)
    advanced_sampling_methods = db.StringField(max_length=200)

    forcefields = db.StringField(max_length=200)
    file_formats = db.StringField(max_length=100)
    qm_mm = db.BooleanField()

    # tags
    TAG_NAMES = [
                "periodicity_0d",
                "periodicity_1_and_2d",
                "periodicity_3d",
                "constraints",
                "rigid_bodies",
                "restraints",
                "monte_carlo",
                "rnemd",     # RNMED
                "analysis_tools",
                "building_tools",
                "implicit_solvent",

                # forcefield
                "class_i",
                "class_ii",
                "polarizable",
                "reactive",
                "inorganic_metals"
    ]

    tags = db.ListField(db.StringField(max_length=20, choices=TAG_NAMES))

    def add_tags(self, kwargs):
        self.tags = []
        for tag in self.TAG_NAMES:
            if tag in kwargs:
                tag_val = kwargs.pop(tag, '')
                if tag_val and tag_val.lower() not in ['', 'no', 'false']:
                    self.tags.append(tag)


class Software(db.DynamicDocument):     # flexible schema, can have extra attributes

    # added by
    added_by_name = db.StringField(max_length=100, required=True)
    added_by_email = db.EmailField(required=True)
    is_SW_owner = db.BooleanField(required=True, default=False)

    # availability
    software_name = db.StringField(max_length=100, required=True)
    license = db.StringField(max_length=200)
    price = db.StringField(max_length=200)
    latest_version = db.StringField(max_length=100)
    date_of_latest_version = db.DateTimeField()                   # Date of latest version
    principal_contact_name = db.StringField(max_length=100)
    principal_contact_email = db.EmailField()
    official_website = db.URLField()

    # Others
    description = db.StringField(required=True, default='')
    long_description = db.StringField(required=True, default='')
    comments = db.StringField()
    required_citation = db.StringField()
    domain = db.StringField(required=True, default='MM', choices=['MM', 'QM'])      # QM, MM, QM/MM, etc..

    # software engineering
    LANGUAGES = ['C', 'C++', 'Python', 'FORTRAN', 'FORTRAN2003', 'FORTRAN77',
                 'FORTRAN90', 'Java', 'JavaScript', 'Other']

    source_code = db.URLField()
    executables = db.StringField(max_length=100)
    code_management = db.StringField(max_length=100)
    continuous_integration = db.StringField(max_length=100)
    tests = db.StringField(max_length=100)
    languages = db.ListField(db.StringField(max_length=20, choices=LANGUAGES))
    # for search efficiency, repeat in lowercase, keep original case for display
    languages_lower = db.ListField(db.StringField(max_length=20))
    compilers = db.StringField(max_length=100)

    # Performance
    parallel = db.StringField(max_length=50, choices=['', 'Yes', 'No'])
    gpu = db.StringField(max_length=50, choices=['', 'Yes', 'No'])
    knl = db.StringField(max_length=50, choices=['', 'Yes', 'No'])

    # support
    support_line = db.StringField(max_length=250)  # url or email
    documentation = db.URLField()
    number_of_tutorials = db.IntField()
    wiki = db.URLField()
    forum = db.URLField()
    mail_list = db.URLField()
    ui = db.BooleanField()

    # Local
    # published = DateTimeField()
    date_added = db.DateTimeField(default=datetime.datetime.now)
    is_pending = db.BooleanField(default=True)

    mm_features = db.EmbeddedDocumentField(MMFeatures)

    qm_features = db.EmbeddedDocumentField(QMFeatures)

    # Use the $ prefix to set a text index
    meta = {
        # 'allow_inheritance': True,  # known issue with text search
        'strict': False,    # allow extra fields
        'indexes': [
            "domain",
            {
                'fields': ['$software_name', "$description", "$long_description"],
                'default_language': "en",
                "language_override": "en",
            }
        ]
    }

    def __unicode__(self):
        return self.software_name

    @property
    def library_type(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        """Override save to add languages_lower"""
        self.add_language_lower()
        return super(Software, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + ', name: ' + self.software_name + ', is_pending: ' + \
                str(self.is_pending) + ', Domain: ' + self.domain

    def add_language_lower(self):
        if self.languages:
            self.languages_lower = [lang.lower() for lang in self.languages]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def props(cls):
    all_props = [i for i in cls.__dict__.keys() if i[:1] != '_']
    all_props.remove('tags')
    all_props.remove('TAG_NAMES')
    all_props.remove('add_tags')
    return all_props


def set_props_values(cls, obj, prop_values):
    for prop in props(cls):
            if prop in prop_values:
                tag_val = prop_values.pop(prop, '')
                if tag_val:  # and tag_val.lower() not in ['', 'no', 'false']:
                    setattr(obj, prop, tag_val)


def create_software(lib_type='', **kwargs):
    """Create a Library object from a set of params
       A Builder Design Pattern"""

    if lib_type == 'MM':
        mm_features = MMFeatures()
        set_props_values(MMFeatures, mm_features, kwargs)
        mm_features.add_tags(kwargs)
        lib = Software(mm_features=mm_features, **kwargs)

    elif lib_type == 'QM':
        qm_features = QMFeatures()
        set_props_values(QMFeatures, qm_features, kwargs)
        qm_features.add_tags(kwargs)
        lib = Software(qm_features=qm_features, **kwargs)

    else:
        lib = Software(**kwargs)

    return lib
