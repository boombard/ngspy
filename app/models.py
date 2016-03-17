from sqlalchemy import Column, Integer, String, ForeignKey, Date
from extensions import db


class IdModel(object):

    id = Column(Integer, nullable=False, primary_key=True)


class Team(db.Model, IdModel):

    __tablename__ = 'team'

    name = Column(String, unique=True)

    users = db.relationship('User', backref=db.backref('team'))


class User(db.Model, IdModel):

    __tablename__ = 'user'

    name = Column(String, unique=True)
    team_id = Column(Integer, ForeignKey('team.id'))


class Experiment(db.Model, IdModel):

    __tablename__ = 'experiment'

    description = Column(String)
    date = Date()
    organism_id = Column(Integer, ForeignKey('organism.id'))

    user_id = Column(Integer, ForeignKey('user.id'))


class Organism(db.Model, IdModel):

    __tablename__ = 'organism'

    common_name = Column(String, nullable=False)
    latin_name = Column(String)

    reference_genomes = db.relationship('ReferenceGenome',
                                        backref=db.backref('organism'))


class ReferenceGenome(db.Model, IdModel):

    __tablename__ = 'reference_genome'

    name = Column(String, nullable=False)
    description = Column(String)
    source = Column(String)
    url = Column(String)

    organism_id = Column(Integer, ForeignKey('organism.id'))


class ReferenceIndex(db.Model, IdModel):

    __tablename__ = 'reference_index'

    reference_type = Column(String)
    location = Column(String)

    reference_genome_id = Column(Integer, ForeignKey('reference_genome.id'))
    tool_id = Column(Integer, ForeignKey('tool.id'))

    tool = db.relationship('Tool')
    reference_genome = db.relationship('ReferenceGenome')


class Tool(db.Model, IdModel):

    __tablename__ = 'tool'

    name = Column(String)
    version = Column(String)
    location = Column(String)
    default_command = Column(String)


class DataSet(db.Model, IdModel):

    __tablename__ = 'dataset'

    location = Column(String)
    filetype = Column(String)

    experiment_id = Column(Integer, ForeignKey('experiment.id'))
    tool_id = Column(Integer, ForeignKey('tool.id'))

    files = db.relationship('DataFile', backref=db.backref('dataset'))


class DataFile(db.Model, IdModel):

    __tablename__ = 'data_file'

    filename = Column(String)
    lane = Column(Integer)
    direction = Column(Integer)
    multiplex = Column(Integer)
    sanger_id = Column(String)

    dataset_id = Column(Integer, ForeignKey('dataset.id'))


