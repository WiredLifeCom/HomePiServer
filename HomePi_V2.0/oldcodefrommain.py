class Zone:
    def __init__(self):
        self.arrival = "2015-04-21T11:42:11.000+02:00"
        self.departure = "2015-04-21T11:58:32.000+02:00"
        self.latitude = 55.61592
        self.longitude = 12.987113


class Inventory:
    def __init__(self):
        self.resources = ["Dirt", "Dirt", "Stone"]
        self.items = ["DiamondPickAxe", "WoodenAxe"]


class User:
    def __init__(self):
        self.username = 'Julian'
        zone = Zone()
        inventory = Inventory()
        self.zones = [zone.__dict__]
        self.inventory = inventory.__dict__


class UserData:
    def __init__(self):
        user = User()
        self.user = user.__dict__
        self.unload = "2015-04-21T13:04:54.000+02:00"
