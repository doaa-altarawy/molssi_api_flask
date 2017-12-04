import datetime
from flask_mongoengine.wtf import model_form
from molssi_api_flask import db


"""
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

    basis = db.StringField()
    coverage = db.StringField()
    other = db.StringField()

    tags = db.ListField(db.StringField())

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

    def add_tags(self, kwargs):
        self.tags = []
        for tag in self.TAG_NAMES:
            if tag in kwargs:
                tag_val = kwargs.pop(tag, '')
                if tag_val and tag_val.lower() not in ['', 'no', 'false']:
                    self.tags.append(tag)


class MMFeatures(db.EmbeddedDocument):
    """MM specific features"""

    ensembles = db.StringField()
    free_energy_methods = db.StringField()
    advanced_sampling_methods = db.StringField()

    forcefields = db.StringField()
    file_formats = db.StringField()
    qm_mm = db.StringField()

    tags = db.ListField(db.StringField())

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

    def add_tags(self, kwargs):
        self.tags = []
        for tag in self.TAG_NAMES:
            if tag in kwargs:
                tag_val = kwargs.pop(tag, '')
                if tag_val and tag_val.lower() not in ['', 'no', 'false']:
                    self.tags.append(tag)


class Library(db.DynamicDocument):     # flexible schema, can have extra attributes

    # availability
    name = db.StringField(required=True)
    owner = db.StringField()
    license = db.StringField()
    price = db.StringField()
    latest_version = db.StringField()
    date = db.DateTimeField()                   # Date of latest version
    principal_contact_name = db.StringField()
    principal_contact_email = db.StringField()
    official_website = db.URLField()

    # Others
    description = db.StringField(required=True, default='')
    long_description = db.StringField(required=True, default='')
    comments = db.StringField()
    required_citation = db.StringField()
    domain = db.StringField(required=True, default='MM')      # QM, MM, QM/MM, etc..

    # software engineering

    source = db.URLField()
    executables = db.StringField()
    code_management = db.StringField()
    continuous_integration = db.StringField()
    tests = db.StringField()
    languages = db.ListField(db.StringField())  #
    # for search efficiency, repeat in lowercase, keep original case for display
    languages_lower = db.ListField(db.StringField())
    compilers = db.StringField()

    # Performance
    parallel = db.StringField()
    gpu = db.StringField()
    knl = db.StringField()

    # support
    support_line = db.StringField()
    documentation = db.StringField()
    tutorials = db.StringField()
    wiki = db.StringField()
    forum = db.StringField()
    mail_list = db.StringField()
    ui = db.StringField()

    # Local
    # published = DateTimeField()
    added = db.DateTimeField(default=datetime.datetime.now)
    is_pending = db.BooleanField(default=False)

    mm_features = db.EmbeddedDocumentField(MMFeatures)

    qm_features = db.EmbeddedDocumentField(QMFeatures)

    # Use the $ prefix to set a text index
    meta = {
        # 'allow_inheritance': True,
        'strict': False,    # allow extra fields
        'indexes': [
            "domain",
            {
                'fields': ['$name', "$description", "$long_description"],
                'default_language': "en",
                "language_override": "en",
            }
        ]
    }

    def __unicode__(self):
        return self.name

    @property
    def library_type(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        """Override save to add languages_lower"""
        self.add_language_lower()
        return super(Library, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + ', name: ' + self.name + ', description: ' + \
                self.description + ', Domain: ' + self.domain

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


def create_library(lib_type='', **kwargs):
    """Create a Library object from a set of params
       A Builder Design Pattern"""

    if lib_type == 'MM':
        mm_features = MMFeatures()
        set_props_values(MMFeatures, mm_features, kwargs)
        mm_features.add_tags(kwargs)
        lib = Library(mm_features=mm_features, **kwargs)

    elif lib_type == 'QM':
        qm_features = QMFeatures()
        set_props_values(QMFeatures, qm_features, kwargs)
        qm_features.add_tags(kwargs)
        lib = Library(qm_features=qm_features, **kwargs)

    else:
        lib = Library(**kwargs)

    return lib
