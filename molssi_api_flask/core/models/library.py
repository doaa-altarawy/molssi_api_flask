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


class Library(db.DynamicDocument):     # flexible schema

    # availability
    name = db.StringField(required=True)
    owner = db.StringField()
    license = db.StringField()
    price = db.StringField()
    latest_version = db.StringField()
    date = db.DateTimeField()      #
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

    # special_fields = EmbeddedDocumentField(ExtrasFieldsAbstractClass)

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

    def __unicode__(self):  # ?
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


class QMLibrary():
    """QM specific features"""

    basis = db.StringField()
    semiempirical = db.StringField()
    dft = db.StringField()
    dft_u = db.StringField()
    hybrid = db.StringField()
    rohf = db.StringField()
    uhf = db.StringField()
    mcscf = db.StringField()
    ci = db.StringField()
    mp_or_mbpt = db.StringField()
    cc = db.StringField()
    rpa = db.StringField()
    gf = db.StringField()
    tddft = db.StringField()
    dmf = db.StringField()
    coverage = db.StringField()
    fequencies_phonons = db.StringField()
    nmr = db.StringField()
    other = db.StringField()
    symmetry = db.StringField()


class MMLibrary():
    """MM specific features"""

    periodicity_0_d = db.StringField()
    periodicity_1_and_2_d = db.StringField()
    periodicity_3_d = db.StringField()
    constraints = db.StringField()
    rigid_bodies = db.StringField()
    restraints = db.StringField()
    ensembles = db.StringField()
    monte_carlo = db.StringField()
    free_energy_methods = db.StringField()
    advanced_sampling_methods = db.StringField()
    rnemd = db.StringField()
    analysis_tools = db.StringField()
    building_tools = db.StringField()
    implicit_solvent = db.StringField()

    # Forcefields

    class_i = db.StringField()
    class_ii = db.StringField()
    polarizable = db.StringField()
    reactive = db.StringField()
    inorganic_metals = db.StringField()
    forcefields = db.StringField()
    file_formats = db.StringField()
    qm_mm = db.StringField()
