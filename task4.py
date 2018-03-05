import random


def get_valid_input(input_string, valid_options):
    '''
    :param input_string: string
    :param valid_options: tuple
    :return: string
    A function looping until user provides a valid input
    from the given options
    '''
    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


class Property:
    '''a class that represents property with its basic charachteristics,
    such as square feet, #of beds and bath'''
    def __init__(self, square_feet='', beds='', baths='', **kwargs):
        '''
        the assembler
        '''
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_baths = baths

    def display(self):
        '''
        similar to __str__ method, used to show the needed info
        '''
        print("PROPERTY DETAILS")
        print("================")
        print("square footage: {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()

    def prompt_init():
        '''
        A method creating a dictionary
        :return: dict
        '''
        return dict(square_feet=input("Enter the square feet: "),
                    beds=input("Enter number of bedrooms: "),
                    baths=input("Enter number of baths: "))
    prompt_init = staticmethod(prompt_init)


class Apartment(Property):
    '''
    inhereted from Property, responsible for apartments with all its features
    '''
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        '''
        again, method dispalying all the info
        return: None
        '''
        super().display()
        print("APARTMENT DETAILS")
        print("laundry: %s" % self.laundry)
        print("has balcony: %s" % self.balcony)

    def prompt_init():
        '''
        updating ancestors info dictionaty
        return: dictionary
        '''
        parent_init = Property.prompt_init()
        laundry = get_valid_input("What laundry facilities does the property have? ",
                                  Apartment.valid_laundries)
        balcony = get_valid_input("Does the property have a balcony? ",
                                  Apartment.valid_balconies)
        parent_init.update({"laundry": laundry, "balcony": balcony})
        return parent_init
    prompt_init = staticmethod(prompt_init)


class House(Property):
    ''' A class representing all kinds of houses'''
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories='', garage='', fenced='', **kwargs):
        '''
        assambler
        :param num_stories: int
        :param garage: str
        :param fenced: str
        :param kwargs:
        '''
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories

    def display(self):
        '''

        :return: None
        '''
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))

    def prompt_init():
        '''

        :return: dictionary
        '''
        parent_init = Property.prompt_init()
        fenced = get_valid_input("Is the yard fenced? ", House.valid_fenced)
        garage = get_valid_input("Is there a garage? ", House.valid_garage)
        num_stories = input("How many stories? ")
        parent_init.update({"fenced": fenced, "garage": garage,
                            "num_stories": num_stories})
        return parent_init
    prompt_init = staticmethod(prompt_init)


class Purchase:
    '''Class allowing agent to sell stuff'''
    def __init__(self, price='', taxes='', **kwargs):
        '''

        :param price: int
        :param taxes: int
        :param kwargs:
        '''
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        '''

        :return: None
        '''
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))

    def prompt_init():
        '''

        :return: dictionary
        '''
        return dict(price=input("What is the selling price? "),
                    taxes=input("What are the estimated taxes? "))

    prompt_init = staticmethod(prompt_init)


class Rental:
    '''Class similar to purcase but with rental options'''
    def __init__(self, furnished='', utilities='', rent='', **kwargs):

        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities

    def display(self):
        '''
        displaying info
        :return: None
        '''
        super().display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(self.utilities))
        print("furnished: {}".format(self.furnished))

    def prompt_init():
        return dict(rent=input("What is the monthly rent? "),
                    utilities=input("What are the estimated utilities? "),
                    furnished=get_valid_input("Is the property furnished? ",
                                              ("yes", "no")))

    prompt_init = staticmethod(prompt_init)


class HouseRental(Rental, House):
    '''Multiple inheretation of house and rental'''
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class ApartmentRental(Rental, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class ApartmentPurchase(Purchase, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class HousePurchase(Purchase, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class Agent:
    '''Class representing an Agent with jobs he can do'''
    def __init__(self):
        '''
        assambler
        '''
        self.property_list = []

    def display_properties(self):
        '''
        displaying properties
        :return: None
        '''
        for property in self.property_list:
            property.display()
    type_map = {("house", "rental"): HouseRental,
                ("house", "purchase"): HousePurchase,
                ("apartment", "rental"): ApartmentRental,
                ("apartment", "purchase"): ApartmentPurchase}

    def add_property(self):
        '''
        method adding property to the list
        :return: None
        '''
        property_type = get_valid_input("What type of property? ",
                                        ("house", "apartment")).lower()
        payment_type = get_valid_input("What payment type? ",
                                       ("purchase", "rental")).lower()
        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))

    def gift_property(self):
        '''
        a method randomly choosing whether you get a free home
        :return: None
        '''
        lst = [True, False]
        ans = get_valid_input("Would you like to win a lottery? ",("yes", "maybe")).lower()
        print("Lets cross your fingers")
        print("Parapapam.....")
        final = random.choice(lst)
        if final:
            if self.property_list:
                print("Yay, this is your new home")
                self.property_list[0].display()
            else:
                print("sorry, I guess its not your lucky day")
        else:
            print("sorry, I guess its not your lucky day")

    def navigation(self):
        '''
        method looking for homes with given radius of square feet
        :return: None
        '''
        ans1 = int(input("What is the approximate # of square_feet you are looking for? "))
        ans = int(input("What precision do you want?"))
        c = 0
        print("Looking for matches....")
        for property in self.property_list:
            if abs(int(property.square_feet) - ans) <= ans1:
                property.display()
                c += 1
        if c == False:
            print("Sorry, no matches for ya")
