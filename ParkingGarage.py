from ui import clearTerminal

class ParkingGarage:
    options = [
        "t",
        "p",
        "l",
        "c",
        "g",
    ]

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
        
        self.optionsDict = {
            ParkingGarage.options[0]: self.takeTicket,
            ParkingGarage.options[1]: self.payForParking,
            ParkingGarage.options[2]: self.leaveGarage,
            ParkingGarage.options[3]: self._garageStatus,
            ParkingGarage.options[4]: self._garageStatus,
        }

    def takeTicket(self):
        if self.availableTickets > 0:
            self._updateTickets()
            return self._giveTicketNumber()

    def payForParking(
        self,
        message="You must have forgotten something... Please enjoy your stay!",
        leaving=False,
    ):
        if emptyMessage := self._checkEmpty():
            return emptyMessage

        ticketNum = self._getUserInput(
            f"{self._showActiveTickets()}Please enter your ticket number: "
        )

        if not ticketNum in self.activeTickets:
            message = "Not an active ticket..."
            if leaving:
                return False, message
            else:
                return message

        if ticketNum == False:
            return False, message

        print(self.tickets)
        if self.tickets[self._getTicketIndex(ticketNum)][ticketNum] == False:
            paid, paymentMessage = self._requestPayment(message)
            self.tickets[self._getTicketIndex(ticketNum)][ticketNum] = paid

            if leaving:
                return ticketNum, paymentMessage
            else:
                return paymentMessage
        else:
            message = f"Ticket #{ticketNum} is already paid for!\n"
            if leaving:
                return ticketNum, message
            else:
                return message

    def leaveGarage(self):
        if emptyMessage := self._checkEmpty():
            return emptyMessage

        ticketNum, message = self.payForParking(
            "*The gate slams shut*\nPlease enjoy your stay!", leaving=True
        )

        if ticketNum and self.tickets[self._getTicketIndex(ticketNum)][ticketNum]:
            self._updateTickets(ticketNum)
            return f"{message}Ticket #{ticketNum} paid and left!"
        else:
            return message

    def garageRunner(self):
        message = ""
        while True:
            baseMessage = "What would you like to do?\n[T]ake ticket/[P]ay for parking/[L]eave garage/[G]arage status/[C]lock out: "
            message = f"{message}{baseMessage}"

            message = self.optionsDict[choice := self._getUserInput(message, True)]()
            message += "\n"

            if choice == "c":
                clearTerminal()
                print(message)
                break

    def _showActiveTickets(self):
        return f"Active tickets: {', '.join([str(ticketNum) for ticketNum in sorted(self.activeTickets)])}\n"

    def _garageStatus(self):
        return f"There are currently {len(self.tickets)} cars parked in the garage.\nToday the garage put out {self.ticketsTaken} tickets and made ${self.ticketPrice * self.ticketsPaid}"

    def _getUserInput(self, message, runner=False, invalid=False):
        def trimUserInput(str):
            return str.lower()[0]

        while True:
            clearTerminal()
            try:
                if invalid:
                    print("Invalid entry...")
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
                    message = "Thank you for your payment!\n"
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
        sortedList = sorted(self.tickets, key=lambda x: list(x.keys())[0])
        print(sortedList)
        self.tickets = sortedList

    def _findLowest(self):
        if len(self.tickets) == 0:
            self.activeTickets.append(1)
            return 1

        nums = []
        for ticket in self.tickets:
            for key in (sortedKeys := sorted(ticket.keys())):
                nums.append(key)

        for i in range(1, sortedKeys[len(sortedKeys) - 1] + 2):
            if not i in nums:
                self.nextTicket = i
                self.activeTickets.append(i)
                return i
