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

        self.select_a_case()
        self.generate_id()

    # losowanie problemu klienta
    def select_a_case(self, cases=['personal account', 'credits', 'loans', 'crisis situation'], probabilities=[0.5, 0.3, 0.25, 0.2]):
        self.case = random.choices(cases, weights=probabilities)
        

    # losowanie czasu potrzebnego na obsluge
    def generate_service_time(self):
        if self.case == ['personal account']:
            self.draw_time(360, 180)
        elif self.case == ['credits']:
            self.draw_time(720, 120)
        elif self.case == ['loans']:
            self.draw_time(600, 120)
        else:
            self.draw_time(900, 180)
        return self.serviceTime

    def draw_time(self, mu, sigma):
        self.serviceTime = random.gauss(mu, sigma)
        while self.serviceTime < 0:
            self.serviceTime = random.gauss(mu, sigma)

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

        if self.currentClient is not None:
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
            print(self.head.case)
            popped = self.head
            self.head = self.head.next
            self.length -= 1
            return popped
        

    def checkStatusEmployees(self):
        for emp in range(len(self.employees)):
            if self.employees[emp].status == 'free' and self.length != 0 and self.employees[emp].statusChangingClient != True:
                self.employees[emp].change_status()
                self.employees[emp].currentClient = self.dequeue()
                if self.employees[emp].check_choice_of_case():
                    return self.employees[emp].currentClient
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
        self.queueAccount = Queue(4)
        self.queueCredit = Queue(3)
        self.queueLoan = Queue(2)
        self.queueCrisis = Queue(2)

        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            self.flowOfClients = 1/240
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=8)
        else:
            self.flowOfClients = 1/480
            self.startTime = datetime.now().replace(
                microsecond=0, second=0, minute=0, hour=9)

    def check_case_of_client(self, client: Client):
        if client.case == ['personal account']:
            self.queueAccount.append_client(client)
            
        elif client.case == ['credits']:
            
            self.queueCredit.append_client(client)
        elif client.case == ['loans']:
            self.queueLoan.append_client(client)
            
        else:
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
                print(client.case)
                self.clientsArrivals.append(now.strftime("%H:%M:%S"))
                self.check_case_of_client(client)
                timeToNextClient = math.ceil(
                    random.expovariate(self.flowOfClients))
                clientArrival = now + timedelta(seconds=timeToNextClient)

            for queue in (self.queueAccount, self.queueCredit, self.queueLoan, self.queueCrisis):
                clientToRedirect = queue.checkStatusEmployees()
                if clientToRedirect:
                    self.check_case_of_client(clientToRedirect)

            for queue in (self.queueAccount, self.queueCredit, self.queueLoan, self.queueCrisis):
                current_client = queue.head
                while current_client:
                    
                    current_client.waitingTime += 1
                    current_client = current_client.next

            

            for employee in self.queueAccount.employees + self.queueCredit.employees + self.queueLoan.employees + self.queueCrisis.employees:
                
                if employee.statusChangingClient == True and employee.breakLeft == 0:
                    employee.statusChangingClient = False
                
                elif employee.statusChangingClient == True and employee.breakLeft > 0:
                    employee.breakLeft -= 1
                
                if employee.status == 'occupied':
                    if employee.timeLeft > 0:
                        employee.timeLeft -= 1
                        if employee.timeLeft == 0:
                            served_client_data = {
                        'id': employee.currentClient.id,
                        'case': str(employee.currentClient.case),
                        'arrival_time': employee.currentClient.arrivalTime,
                        'waiting_time': employee.currentClient.waitingTime,
                        'service_time': employee.currentClient.serviceTime
                        }
                            self.clients_data.append(served_client_data)
                            employee.change_status()
                            employee.statusChangingClient = True
                            employee.breakLeft = 15

            current += 1

        print(self.clientsArrivals)
        print("Clients data:", self.clients_data)

sim = Simulation('saturday')
sim.simulate(2)
