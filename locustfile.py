from locust import HttpUser, task, between

class GUDLFTUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(1)
    def index_page(self):
        self.client.get("/")
    
    @task(2)
    def login(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
    
    @task(3)
    def book_places(self):
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "2"
        })