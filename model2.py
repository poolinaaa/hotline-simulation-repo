import random
import time
from datetime import timedelta, datetime
import math

# klasa klient


class Client:
    id = 0

    def __init__(self, arrivalTime):

        # czas w którym klient pojawił się w systemie
        self.arrivalTime = arrivalTime
        # czas w kolejce / przełączania do innego specjalisty
        self.waitingTime = 0
        # czas obsługi
        self.serviceTime = 0
        self.next = None
        self.previous = None
        self.redirected = False

        self.select_a_case()
        self.generate_id()

    # losowanie problemu klienta
    def select_a_case(self, cases=['personal account', 'credits', 'loans', 'crisis situation'], probabilities=[0.5, 0.3, 0.25, 0.2]):
        self.case = random.choices(cases, weights=probabilities)

    # losowanie czasu potrzebnego na obsluge

    def generate_service_time(self):
        if self.case == ['personal account']:
            self.draw_time(100, 20)
        elif self.case == ['credits']:
            self.draw_time(300, 120)
        elif self.case == ['loans']:
            self.draw_time(500, 120)
        else:
            self.draw_time(600, 180)
        return self.serviceTime

    def draw_time(self, mu, sigma):
        self.serviceTime = math.ceil(random.gauss(mu, sigma))
        while self.serviceTime < 0:
            self.serviceTime = math.ceil(random.gauss(mu, sigma))

    # indywidualny nr klienta

    def generate_id(self):
        self.id = Client.id
        Client.id += 1

    def __str__(self):
        return self.case


class Employee:
    def __init__(self):
        self.status = 'free'
        self.currentClient = None
        self.timeLeft = 0
        self.statusChangingClient = False
        self.breakLeft = 0

    def changeClient(self):
        self.timeLeft += 60

    def change_status(self):
        if self.status == 'free':
            self.status = 'occupied'

        else:
            self.status = 'free'

# 20 procent szans że klient wybrał źle kolejkę
    def check_choice_of_case(self):
        probMistake = 0.2
        randNumber = random.uniform(0, 1)

        if self.currentClient:
            # klient źle wybrał
            if randNumber <= probMistake:
                
                self.changeClient()
                return True
            # klient dobrze wybrał
            else:
                serviceTime = self.currentClient.generate_service_time()
                self.timeLeft = serviceTime
                return False

    

class Queue:
    def __init__(self, amountOfSpecialists):

        self.head = None
        self.tail = None
        self.length = 0
        self.employees = [Employee() for _ in range(amountOfSpecialists)]

    def append_client(self, Client: Client):
        if self.tail == None:
            self.head = Client
            self.tail = Client
            self.length += 1
        else:
            self.tail.next = Client
            self.tail = Client
            self.length += 1

    def dequeue(self):
        if self.head != None:
            print(self.head.case)
            popped = self.head
            if self.head.next != None:
                self.head = self.head.next
            else:
                
                self.head = None
                self.tail = None

            self.length -= 1
            return popped

    

    def checkStatusEmployeesGeneral(self):
        for emp in range(len(self.employees)):
            if self.employees[emp].status == 'free' and self.length != 0 and self.employees[emp].statusChangingClient != True:
                self.employees[emp].change_status()
                self.employees[emp].currentClient = self.dequeue()
                if self.employees[emp].check_choice_of_case():
                    toRedirect = self.employees[emp].currentClient
                    self.employees[emp].currentClient = None
                    print(f"redirected {toRedirect.id}")
                    print()
                    toRedirect.redirected = True
                    print(toRedirect.redirected)
                    return toRedirect
                else:
                    return False
                
    def checkStatusEmployeesTough(self):
        for emp in range(len(self.employees)):
            if self.employees[emp].status == 'free' and self.length != 0 and self.employees[emp].statusChangingClient != True:
                self.employees[emp].change_status()
                self.employees[emp].currentClient = self.dequeue()
                serviceTime = self.employees[emp].currentClient.generate_service_time()
                self.employees[emp].timeLeft = serviceTime
                print(f'czas obslugi {self.employees[emp].timeLeft}')
                
    def size(self):
        print(f'Current length of the queue is {self.length}')

    def front(self):
        if self.head != None:
            print(f'Current front is {self.head.id}')
        else:
            print('Queue is empty')

    def __str__(self):
        listOfClients = []
        if self.head == None:
            return 'Queue is empty :('
        else:
            current = self.head
            while current:
                listOfClients.append(str(current.id))
                current = current.next
            return ', '.join(listOfClients)


# zakladam 4 specjalistów konta, 3 kredyty, 2 pozyczki i 2 kryzys
# 20 procent szans że klient wybrał źle kolejkę

class Simulation:

    def __init__(self, day: str):
        self.clientsArrivals = []
        self.clients_data = []
        self.queueGeneral = Queue(1)
        self.queueToughCase = Queue(2)

        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            self.flowOfClients = 1/240
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=8)
        else:
            self.flowOfClients = 1/480
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=9)


    def simulate(self, timeToSimulate):
        current = 0
        now = self.startTime
        timeToNextClient = math.ceil(random.expovariate(self.flowOfClients))
        clientArrival = self.startTime + timedelta(seconds=timeToNextClient)

        while current < timeToSimulate * 3600:
            
            now = self.startTime + timedelta(seconds=current)
            if now == clientArrival:
                client = Client(now)
                print(client.id)
                self.clientsArrivals.append(now.strftime("%H:%M:%S"))
                self.queueGeneral.append_client(client)
                timeToNextClient = math.ceil(
                    random.expovariate(self.flowOfClients))
                clientArrival = now + timedelta(seconds=timeToNextClient)
                
            
            clientToRedirect = self.queueGeneral.checkStatusEmployeesGeneral()
            self.queueToughCase.checkStatusEmployeesTough()
            if clientToRedirect:
            
                self.queueToughCase.append_client(clientToRedirect)
                print(self.queueToughCase)

            for queue in (self.queueGeneral, self.queueToughCase):
                current_clients = queue.head
                while current_clients:

                    current_clients.waitingTime += 1
                    current_clients = current_clients.next

            for employee in self.queueGeneral.employees + self.queueToughCase.employees:

                if employee.statusChangingClient == True and employee.timeLeft == 0:
                    employee.statusChangingClient = False

                elif employee.statusChangingClient == True and employee.timeLeft > 0:
                    employee.timeLeft -= 1

                if employee.status == 'occupied':
                    if employee.timeLeft > 0:
                        employee.timeLeft -= 1
                        if employee.timeLeft == 0 and employee.currentClient != None:
                            served_client_data = {
                                'id': employee.currentClient.id,
                                'redirected': employee.currentClient.redirected,
                                'case': str(employee.currentClient.case),
                                'arrival_time': employee.currentClient.arrivalTime.strftime("%H:%M:%S"),
                                'waiting_time': employee.currentClient.waitingTime,
                                'service_time': employee.currentClient.serviceTime
                            }
                            self.clients_data.append(served_client_data)
                            

                            employee.change_status()
                            print(employee.status)
                            employee.currentClient = None
                            employee.statusChangingClient = True
                            employee.timeLeft = 15
                        elif employee.timeLeft == 0 and employee.currentClient == None:
                            employee.change_status()
            current += 1
        print(self.clientsArrivals)
        print("Clients data:", self.clients_data)


sim = Simulation('saturday')
sim.simulate(2)
