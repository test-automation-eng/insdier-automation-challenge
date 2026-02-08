from locust import HttpUser, task, between

class N11SearchUser(HttpUser):
    host = "https://www.n11.com"
    wait_time = between(1, 2)

    @task
    def search_iphone(self):
        self.client.get("/arama?q=iphone", name="search_iphone")
            
    @task
    def search_no_results(self):
        self.client.get("/arama?q=asdasdzzqweqwe999", name="search_no_results")