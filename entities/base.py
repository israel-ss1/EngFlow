# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Criamos um objeto MetaData informando o schema 'engflow'.
# Isso fará com que o SQLAlchemy procure todas as tabelas dentro desse schema no Postgres.
metadata = MetaData(schema="engflow")

# Centralizamos a base passando o metadata configurado.
# Todas as classes na pasta 'entities' que herdam de Base agora sabem que pertencem ao schema 'engflow'.
Base = declarative_base(metadata=metadata)