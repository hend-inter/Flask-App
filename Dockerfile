FROM python:3.7
RUN mkdir /src/app/
WORKDIR /src/app/
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["python","/src/app/database/db_create.py"]
CMD ["python","App.py"]
