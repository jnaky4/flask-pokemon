from sqlalchemy import Column, Integer, String, Float
from Models import db


class Base_Stat(db.Model):
    __tablename__ = "Stats"
    dexnum = Column(Integer, primary_key=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)

    def __repr__(self):
        return "<Base_Stats(dexnum=%d, hp=%d, attack=%d, defense=%d," \
               "special_attack=%d, special_defense=%d, speed=%d)>" % \
               (self.dexnum, self.hp, self.attack, self.defense, self.special_attack,
                self.special_defense, self.speed)
