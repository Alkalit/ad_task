# The task description
https://gist.github.com/kotik-adjust/4883e33c439db6de582fd0986939045c

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

`uvicorn --factory "src.project.main:main"`

my contact in telegram: @watercollector
