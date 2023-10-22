from ui import clearTerminal

class ParkingGarage:
    options = [
        "t",
        "p",
        "l",
        "c",
        "g",
    ]
    
    runnerMessage = "What would you like to do?\n[T]icket / [P]ayment / [L]eaving / [G]arage status / [C]lock out: "

    def __init__(self, totalSpaces=50):
        self.parkingSpaces = []
        self.tickets = []
        self.totalSpaces = totalSpaces
        self.availableTickets = totalSpaces
        self.ticketPrice = 5
        self.ticketsTaken = 0
        self.ticketsPaid = 0
        self.nextTicket = 1
        self.activeTickets = []

        # methods in order for optionsDict
        methods = [self.takeTicket, self.payForParking, self.leaveGarage, self._garageStatus, self._garageStatus]
        # generated optionsDict based on given methods and desired character entries
        self.optionsDict = {option: method for option, method in zip(ParkingGarage.options, methods)}


    def takeTicket(self):
        if self.availableTickets > 0:
            self._updateTickets()
            return self._giveTicketNumber()
        else:
            return "We're sorry, the garage is full..."

    def payForParking(
        self,
        message="You must have forgotten something... Please enjoy your stay!",
        leaving=False,
    ):
        if emptyMessage := self._checkEmpty(): # check if the garage is empty before asking for a ticket to pay
            return emptyMessage

        # get the ticket number from the user
        ticketNum = self._getUserInput(
            f"{self._showActiveTickets()}Please enter your ticket number: "
        )

        if not ticketNum in self.activeTickets: # if the ticket number given by the user isn't in the list of active tickets
            message = "Not an active ticket..."
            if leaving: # if payForParking was called from the leaveGarage method
                return False, message
            else:
                return message

        if ticketNum == False: # if the user chose to exit
            return False, message

        if self.tickets[self._getTicketIndex(ticketNum)][ticketNum] == False: # if the ticket is unpaid
            paid, paymentMessage = self._requestPayment(message) # request payment, paid will be true if they choose to pay, else false
            self.tickets[self._getTicketIndex(ticketNum)][ticketNum] = paid # set the ticket to paid or leave it as unpaid

            if leaving:
                return ticketNum, paymentMessage
            else: # if the user isn't paying while leaving, notify them they need to leave soon
                messageEnd = "You have 15 minutes to exit the garage." if paid else ''
                return f"{paymentMessage}{messageEnd}"
        else:
            message = f"Ticket #{ticketNum} is already paid for!"
            if leaving:
                return ticketNum, message
            else:
                return message

    def leaveGarage(self):
        if emptyMessage := self._checkEmpty(): # check if the garage is empty
            return emptyMessage

        ticketNum, message = self.payForParking(
            "*The gate slams shut*\nPlease enjoy your stay!", leaving=True
        )

        if ticketNum and self.tickets[self._getTicketIndex(ticketNum)][ticketNum]: # if the user provides a valid ticket number
            self._updateTickets(ticketNum)

            finalMessage = f"{message}\nTicket #{ticketNum} left!" if message == f"Ticket #{ticketNum} is already paid for!" else f"{message}Ticket #{ticketNum} paid and left!"
            return finalMessage
        else: # if the user doesn't provide a valid ticket number or chooses to remain in the garage
            return message

    def garageRunner(self):
        message = ""
        while True:
            baseMessage = ParkingGarage.runnerMessage
            middleMod = '' if message == "" else '\n'
            message = f"{message}{middleMod}{baseMessage}"

            message = self.optionsDict[choice := self._getUserInput(message, True)]()
            message += "\n"

            if choice == "c":
                clearTerminal()
                print(message)
                break

    def _showActiveTickets(self):
        return f"Active tickets: {', '.join([str(ticketNum) for ticketNum in sorted(self.activeTickets)])}\n"

    def _garageStatus(self):
        """shows number of tickets served, cars currently in garage and money made"""
        return f"{self._showActiveTickets() if len(self.activeTickets) > 0 else ''}There are currently {len(self.tickets)} cars parked in the garage.\nToday the garage put out {self.ticketsTaken} ticket{'' if self.ticketsTaken == 1 else 's'} and made ${self.ticketPrice * self.ticketsPaid}"

    def _getUserInput(self, message, runner=False):
        """takes a message to print to prompt for input, then filters
        
        optional bool arg for if called in runner to filter for runner inputs"""
        def trimUserInput(str):
            return str.lower()[0]
        
        invalid = False

        while True:
            clearTerminal()
            try:
                if invalid:
                    print("Invalid entry...\n")
                    if runner:
                        message = ParkingGarage.runnerMessage
                userInput = input(message)
                invalid = False

                if runner:
                    if (
                        inputToReturn := trimUserInput(userInput)
                    ) in ParkingGarage.options:
                        return inputToReturn
                    else:
                        invalid = True
                        continue

                if trimUserInput(userInput) == "e":
                    return False
                else:
                    return int(userInput)
            except:
                invalid = True
                continue

    def _checkEmpty(self):
        """If the garage is currently empty return an empty garage message"""
        if len(self.activeTickets) == 0:
            return "The garage is currently empty..."

    def _requestPayment(self, message="", payment=0, error=False):
        while payment < 5:
            payment = self._getUserInput(
                f"{message if error else ''}Your amount due is ${self.ticketPrice}\nInsert cash? (bills only)('Exit' to stay in the garage): "
            )
            error = False
            if payment == False:
                return False, message

            if payment >= 5:
                self.ticketsPaid += 1
                if payment == 5:
                    message = f"Thank you for your payment!\n"
                elif payment > 5:
                    message = f"Thank you for your payment!\nYour change is ${payment - self.ticketPrice}\n"
                return True, message
            else:
                if payment < 5 and payment > 0:
                    message = f"Your money has been returned to you... restarting...\n"
                error = True
                continue

    def _giveTicketNumber(self):
        return f"Your ticket # is {self.nextTicket}"

    def _updateTickets(self, ticketNum=False):
        """pass a ticket number (tickets index) to remove the ticket from the list

        otherwise add a new ticket to the tickets list"""

        def updateAvailableTickets():
            self.availableTickets = self.totalSpaces - len(self.tickets)

        if not ticketNum:
            self.tickets.append({self._findLowest(): False})
            self.ticketsTaken += 1
        else:
            del self.tickets[self._getTicketIndex(ticketNum)]
            self.activeTickets.remove(ticketNum)

        self._sortList()

        updateAvailableTickets()

    def _getTicketIndex(self, ticketNum):
        for i, ticket in enumerate(self.tickets):
            if list(ticket.keys())[0] == ticketNum:
                return i

    def _sortList(self):
        """sort the ticket list by key in data structure List[Dict{key:value}]"""
        sortedList = sorted(self.tickets, key=lambda x: list(x.keys())[0])

        self.tickets = sortedList

    def _findLowest(self):
        """Finds the lowest missing ticket in consecutive numbers"""
        if len(self.tickets) == 0:
            self.activeTickets.append(1)
            return 1

        nums = []
        for ticket in self.tickets:
            for key in (sortedKeys := sorted(ticket.keys())): # populate the nums list with sorted keys from the tickets list
                nums.append(key)

        for i in range(1, sortedKeys[len(sortedKeys) - 1] + 2):
            if not i in nums:
                self.nextTicket = i
                self.activeTickets.append(i)
                return i
