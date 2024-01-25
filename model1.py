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
        self.served = False
        self.id = None
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
    id = 0

    def __init__(self):
        self.status = 'free'
        self.currentClient = None
        self.timeLeft = 0
        self.statusChangingClient = False
        self.generate_id()

    def generate_id(self):
        self.id = Employee.id
        Employee.id += 1

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
                wrongCase = self.currentClient.case
                self.currentClient.select_a_case(cases=list(set(['personal account', 'credits', 'loans', 'crisis situation'])-set(wrongCase)),
                                                 probabilities=[1, 1, 1])
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

            popped = self.head
            if self.head.next != None:
                self.head = self.head.next
            else:

                self.head = None
                self.tail = None

            self.length -= 1
            return popped

    # sprawdzanie czy można zacząc obsługiwać kolejnego

    def checkStatusEmployees(self):
        for emp in range(len(self.employees)):
            if self.employees[emp].status == 'free' and self.length != 0 and self.employees[emp].statusChangingClient != True:
                # Zmiana statusu na occupied
                self.employees[emp].change_status()

                # Usunięcie klienta z kolejki
                self.employees[emp].currentClient = self.dequeue()

                if self.employees[emp].check_choice_of_case():
                    toRedirect = self.employees[emp].currentClient
                    self.employees[emp].currentClient = None

                    return toRedirect
                else:
                    return False

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
        self.queueAccount = Queue(3)
        self.queueCredit = Queue(2)
        self.queueLoan = Queue(2)
        self.queueCrisis = Queue(1)

        if day in ('monday'):
            self.flowOfClients = 1/60
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=8)

        if day in ('tuesday', 'wednesday', 'thursday'):
            self.flowOfClients = 1/80
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=8)

        if day in ('friday'):
            self.flowOfClients = 1/65
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=8)

        else:
            self.flowOfClients = 1/70
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=9)

    def check_case_of_client(self, client: Client):
        if client.case == ['personal account']:
            self.queueAccount.append_client(client)

        elif client.case == ['credits']:

            self.queueCredit.append_client(client)
        elif client.case == ['loans']:
            self.queueLoan.append_client(client)

        elif client.case == ['crisis situation']:
            self.queueCrisis.append_client(client)

    def simulate(self, timeToSimulate):
        current = 0
        now = self.startTime
        timeToNextClient = math.ceil(random.expovariate(self.flowOfClients))
        clientArrival = self.startTime + timedelta(seconds=timeToNextClient)

        while current < timeToSimulate * 3600:

            now = self.startTime + timedelta(seconds=current)

            if now == clientArrival:
                client = Client(now)

                self.clientsArrivals.append(now.strftime("%H:%M:%S"))
                self.check_case_of_client(client)
                timeToNextClient = math.ceil(
                    random.expovariate(self.flowOfClients))
                clientArrival = now + timedelta(seconds=timeToNextClient)

            # sprawdzanie w każdej kolejce czy można obsłużyć kolejnego klienta
            for queue in (self.queueAccount, self.queueCredit, self.queueLoan, self.queueCrisis):
                # jeśli pracownik dostaje klienta to sprawdza czy klient wybrał dobrze kolejkę
                clientToRedirect = queue.checkStatusEmployees()
                if clientToRedirect:
                    self.check_case_of_client(clientToRedirect)

            # zwiększanie czasu oczekiwania klientom w kolejkach
            for queue in (self.queueAccount, self.queueCredit, self.queueLoan, self.queueCrisis):
                current_client = queue.head
                while current_client:

                    current_client.waitingTime += 1
                    current_client = current_client.next

            for employee in self.queueAccount.employees + self.queueCredit.employees + self.queueLoan.employees + self.queueCrisis.employees:

                if employee.statusChangingClient == True and employee.timeLeft == 0:

                    employee.statusChangingClient = False

                elif employee.statusChangingClient == True and employee.timeLeft > 0:
                    employee.timeLeft -= 1

                if employee.status == 'occupied':
                    if employee.timeLeft > 0:
                        employee.timeLeft -= 1
                        if employee.timeLeft == 0 and employee.currentClient != None and employee.statusChangingClient != True:

                            served_client_data = {
                                'id': employee.currentClient.id,
                                'case': str(employee.currentClient.case),
                                'arrival_time': employee.currentClient.arrivalTime.strftime("%H:%M:%S"),
                                'waiting_time': employee.currentClient.waitingTime,
                                'service_time': employee.currentClient.serviceTime,
                                'employee id': employee.id
                            }
                            self.clients_data.append(served_client_data)
                            served_client_data = {}

                            employee.change_status()

                            employee.currentClient = None

                            employee.statusChangingClient = True
                            employee.timeLeft = 15
                        elif employee.timeLeft == 0 and employee.currentClient == None:
                            employee.change_status()
            current += 1

        print("Clients data:", self.clients_data)


sim = Simulation('friday')
sim.simulate(3)
print('finiszed')
