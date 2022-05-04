FROM mrosales/python-poetry

COPY src/ /opt/src/
ADD poetry.lock /opt/
ADD pyproject.toml /opt/

WORKDIR /opt/

RUN poetry install

EXPOSE 8000

CMD poetry run uvicorn src.api.main:app --port=8000 --reload