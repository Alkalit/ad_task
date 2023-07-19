from locust import HttpUser, task, between


class User(HttpUser):

    @task
    def root(self):
        self.client.get("")

    @task
    def show_group_by_channel_and_country(self):
        self.client.get("/?date_from=2017-06-01&sort=clicks&groupby=channel&groupby=country&ordering=desc")

    @task
    def show_group_by_date(self):
        self.client.get("/?date_from=2017-05-01&date_to=2017-06-01&os=ios&sort=date&groupby=date&ordering=asc")

    @task
    def show_group_by_os(self):
        self.client.get("/?date_from=2017-06-01&date_to=2017-06-02&countries=US&sort=revenue&groupby=os&ordering=desc")

    @task
    def show_group_by_channel(self):
        self.client.get("/?countries=CA&sort=cpi&groupby=channel&ordering=desc")
