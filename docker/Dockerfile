FROM python:3.6

RUN git clone https://github.com/mgawino/cloud_file_manager.git
WORKDIR cloud_file_manager
RUN python setup.py install
RUN pip install -r requirements.txt

CMD python cloud_file_manager/web/app.py