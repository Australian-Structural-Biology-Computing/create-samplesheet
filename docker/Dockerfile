FROM python:3.9-slim

LABEL authors="Nathan Glades <n.glades@unsw.edu.au>" \
	title="Australian-Structural-Biology-Computing/create-samplesheet" \
	Version="1.1" \
	description="Dockerfile containing samplesheetutils"

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	build-essential \
	procps

RUN pip install samplesheetutils==1.1
