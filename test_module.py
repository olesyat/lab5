import task4

init = task4.HouseRental.prompt_init()
house = task4.HouseRental(**init)
house.display()
agent = task4.Agent()
agent.add_property()
agent.display_properties()
agent.gift_property()
agent.gift_property()
agent.navigation()
agent.navigation()
