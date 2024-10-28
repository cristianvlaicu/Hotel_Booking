import pandas

# Load hotel data, ensuring 'id' column is treated as strings
df = pandas.read_csv("hotels.csv", dtype={"id": str})
# Load credit card data as a list of dictionaries
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
# Load credit card security data, ensuring all columns are treated as strings
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    """
    Represents a hotel with basic information and booking functionality.
    """
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class SpaHotel(Hotel):
    """
    Represents a hotel with a spa, inheriting from the Hotel class.
    """
    def book_spa_package(self):
        """Placeholder for booking a spa package."""
        pass


class ReservationTicket:
    """
    Generates a reservation ticket for a hotel booking.
    """
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        """Generates the content of the reservation ticket."""
        content = f"""
        Thank you for reservation!
        Here are your booking data: 
        Name: {self.customer_name.title()}
        Hotel Name: {self.hotel.name}
"""
        return content


class CreditCard:
    """
    Represents a credit card with basic validation.
    """
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        """Validates the credit card information against a database."""
        card_data = {
            "number": self.number,
            "expiration": expiration,
            "holder": holder,
            "cvc": cvc,
        }
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    """
    Represents a credit card with additional security authentication.
    """
    def authenticate(self, given_password):
        """Authenticates the credit card using a password."""
        password = df_cards_security.loc[
            df_cards_security["number"] == self.number, "password"
        ].squeeze()
        if password == given_password:
            return True
        else:
            return False


class SpaTicket:
    """
    Generates a ticket for a spa reservation.
    """
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        """Generates the content of the spa ticket."""
        content = f"""
        Thank you for your SPA reservation!
        Here are you SPA booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


# Display the hotel data
print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(
        expiration="12/26", holder="JOHN SMITH", cvc="123"
    ):
        if credit_card.authenticate(given_password="mypass1"):
            hotel.book()
            name = input("Enter your name please: ")
            reservation_ticket = ReservationTicket(
                customer_name=name, hotel_object=hotel
            )
            print(reservation_ticket.generate())
            spa = input("Do you want to book a spa package? ")
            if spa == "yes":
                hotel.book_spa_package()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())
        else:
            print("Credit card authentication failed. Sorry!")
    else:
        print("There was a problem with your payment. Sorry!")
else:
    print("Hotel is not available. Sorry!")