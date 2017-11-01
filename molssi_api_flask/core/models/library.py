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


class Library(DynamicDocument):     # flexible schema

    # availability
    name = StringField(required=True)
    owner = StringField()
    license = StringField()
    price = StringField()
    latest_version = StringField()
    date = DateTimeField()      #
    principal_contact_name = StringField()
    principal_contact_email = StringField()
    official_website = StringField()

    # Others
    description = StringField()
    long_description = StringField()
    comments = StringField()
    required_citation = StringField()
    domain = StringField()      # QM, MM, QM/MM, etc..

    # software engineering

    source = StringField()
    executables = StringField()
    code_management = StringField()
    continuous_integration = StringField()
    tests = StringField()
    languages = ListField(StringField())  #
    compilers = StringField()

    # Performance
    parallel = StringField()
    gpu = StringField()
    knl = StringField()

    # support
    support_line = StringField()
    documentation = StringField()
    tutorials = StringField()
    wiki = StringField()
    forum = StringField()
    mail_list = StringField()
    ui = StringField()

    # Local
    # published = DateTimeField()
    added = DateTimeField(default=datetime.datetime.now)
    is_pending = BooleanField(default=False)

    # Use the $ prefix to set a text index
    meta = {
        'allow_inheritance': True,
        # 'strict': False,  # allow extra fields
        'indexes': [{
                'fields': ['$name', "$description", "$long_description", "domain"],
                'default_language': "en",
                "language_override": "en",
        }]
    }

    def __str__(self):
        return str(self.id) + ', name: ' + self.name + ', description: ' + \
                self.description + ', Domain: ' + self.domain


class QMLibrary(Library):
    """QM specific features"""

    basis = StringField()
    semiempirical = StringField()
    dft = StringField()
    dft_u = StringField()
    hybrid = StringField()
    rohf = StringField()
    uhf = StringField()
    mcscf = StringField()
    ci = StringField()
    mp_or_mbpt = StringField()
    cc = StringField()
    rpa = StringField()
    gf = StringField()
    tddft = StringField()
    dmf = StringField()
    coverage = StringField()
    fequencies_phonons = StringField()
    nmr = StringField()
    other = StringField()
    symmetry = StringField()


class MMLibrary(Library):
    """MM specific features"""

    periodicity_0_d = StringField()
    periodicity_1_and_2_d = StringField()
    periodicity_3_d = StringField()
    constraints = StringField()
    rigid_bodies = StringField()
    restraints = StringField()
    ensembles = StringField()
    monte_carlo = StringField()
    free_energy_methods = StringField()
    advanced_sampling_methods = StringField()
    rnemd = StringField()
    analysis_tools = StringField()
    building_tools = StringField()
    implicit_solvent = StringField()

    # Forcefields

    class_i = StringField()
    class_ii = StringField()
    polarizable = StringField()
    reactive = StringField()
    inorganic_metals = StringField()
    forcefields = StringField()
    file_formats = StringField()
    qm_mm = StringField()
