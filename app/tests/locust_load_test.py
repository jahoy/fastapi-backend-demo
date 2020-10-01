from locust import HttpLocust, TaskSet, task


class BookstoreLocustTasks(TaskSet):
    # @task
    # def token_test(self):
    #     self.client.post("/token", dict(username="test", password="test"))

    @task
    def test_post_user(self):
        user_dict = {
            "name": "personel1",
            "password": "pass1",
            "role": "admin",
            "mail": "a@b.com",
        }
        auth_header = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyZGIiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE1NzE5ODE2Mzd9.10lKu4h4a8cKOzAGREb8XZWFgoctgDHBI4m_CpD9Bmw"
        }
        self.client.post("/v1/user", json=user_dict, headers=auth_header)


class BookstoreLoadTest(HttpLocust):
    task_set = BookstoreLocustTasks
    host = "http://138.68.122.72:80"
