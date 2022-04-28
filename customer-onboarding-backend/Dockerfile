FROM python:3.9
WORKDIR /
COPY . .
RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN pip install requirements/sac_configurations-2.0.2-py3-none-any.whl requirements/sac_log-2.0.0-py3-none-any.whl
RUN pip install -r requirements.txt
CMD ["python", "run.py"]