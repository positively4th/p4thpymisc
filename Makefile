.PHONY: requirements all

all: 
	make requirements
	
requirements: 
	python -m venv .venv
	(source .venv/bin/activate && pip install --upgrade pip  && pip install -r requirements.txt)


clean: 
	rm -rf .venv


