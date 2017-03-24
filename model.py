import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

engine = sa.create_engine('sqlite:///music.db', echo=True)

Base = declarative_base()

SessionMaker = sa.orm.sessionmaker(bind=engine)
session = SessionMaker()


class Band(Base):
    __tablename__ = 'bands'

    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.Unicode(255), nullable=False, unique=True)

    def __str__(self):
        return '<Album id={0.id} name={0.name}>'.format(self)


class Album(Base):
    __tablename__ = 'albums'

    id = sa.Column(sa.Integer, primary_key=True)

    title = sa.Column(sa.Unicode(255), nullable=False)
    release_date = sa.Column(sa.Date)
    band_id = sa.Column(sa.ForeignKey(Band.id, ondelete='cascade'), nullable=False)

    band = sa.orm.relationship(Band, backref='albums')

    def __str__(self):
        return '<Album id={0.id} title={0.title} band={0.band}>'.format(self)


class Song(Base):
    __tablename__ = 'songs'

    id = sa.Column(sa.Integer, primary_key=True)

    title = sa.Column(sa.Unicode(255), nullable=False)
    track_num = sa.Column(sa.Integer, nullable=False)
    length_seconds = sa.Column(sa.Float, nullable=False)

    album_id = sa.Column(sa.ForeignKey(Album.id, ondelete='cascade'), nullable=False)

    album = sa.orm.relationship(Album, backref=sa.orm.backref('songs', order_by=track_num))

    def __str__(self):
        return '<Song id={0.id} track_num={0.track_num} album={0.album}>'.format(self)


Base.metadata.create_all(engine)
