# tl;dr the urls:
- http://127.0.0.1:8000/?date_from=2017-06-01&sort=clicks&groupby=channel&groupby=country&ordering=desc
- http://127.0.0.1:8000/?date_from=2017-05-01&date_to=2017-06-01&os=ios&sort=date&groupby=date&ordering=asc
- http://127.0.0.1:8000/?date_from=2017-06-01&date_to=2017-06-02&countries=US&sort=revenue&groupby=os&ordering=desc
- http://127.0.0.1:8000/?countries=CA&sort=cpi&groupby=channel&ordering=desc


# Installation and launch:
`git clone https://github.com/Alkalit/ad_task.git`

in the project directory:

`pip install -e .` requires pip version >= 23

`alembic upgrade head`

`gunicorn "src.project.main:main()" -w 32 -k uvicorn.workers.UvicornWorker`
`gunicorn src.project.main:app -w 32 -k uvicorn.workers.UvicornWorker`

my contact in telegram: @watercollector