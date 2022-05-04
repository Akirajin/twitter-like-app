FROM mrosales/python-poetry

COPY features/ /opt/features
ADD poetry.lock /opt/
ADD pyproject.toml /opt/

WORKDIR /opt/

RUN poetry install

CMD poetry run behave