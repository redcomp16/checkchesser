class Player:
    def __init__(self, name, school, grade, uscf_id):
        self.name = name
        self.school = school
        self.grade = grade
        self.uscf_id = uscf_id
        self.main_link = self.get_main_link()
        self.history_link = self.get_history_link()
        self.official_rating = None
        self.live_rating = None
        self.delta_live_rating = None

    def get_main_link(self):
        main_link = f"https://ratings-api.uschess.org/api/v1/members/{self.uscf_id}"
        return main_link
    
    def get_history_link(self):
        history_link = f"https://ratings-api.uschess.org/api/v1/members/{self.uscf_id}/sections"
        return history_link

    def __repr__(self):
        return (
            f"Player(name={self.name}, uscf_id={self.uscf_id}, school={self.school}, grade={self.grade}, official_rating={self.official_rating}, live_rating={self.live_rating}, delta_live_rating={self.delta_live_rating})"
        )
