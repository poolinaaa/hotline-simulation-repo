import random
import time
from datetime import timedelta, datetime


class Client:
    id = 0
    
    def __init__(self, arrivalTime):
        
        self.arrivalTime = arrivalTime
        self.waitingTime = 0
        self.serviceTime = 0
        self.next = None
        self.previous = None
        self.select_a_case()
        
    def select_a_case(self):
        cases = ['personal account', 'credits', 'loans', 'crisis situation']
        probabilities = [0.5, 0.3, 0.25, 0.2]
        self.case = random.choices(cases, weights=probabilities)
    
    def generate_service_time(self):
        pass
    
    def generate_id(self):
        self.id = id
        Client.id += 1
        
    def __str__(self):
        return self.case

class Employee:
    def __init__(self):
        self.status = 'free'
        self.currentClient = None
        self.timeLeft = 0
    
    def changeClient(self):
        self.timeLeft += 1
        
    def change_status(self):
        if self.status == 'free':
            self.status = 'occupied'
        else:
            self.status = 'free'
            
#20 procent szans że klient wybrał źle kolejkę           
    def check_if_clients_choice_of_case(self):
        pass
#tutaj też zaktualizuje czas pracownika          
    
    
 
class Queue:
    def __init__(self, amountOfSpecialists):
        
        self.head = None
        self.tail = None
        self.length = 0
        self.employees = [Employee() for _ in range(amountOfSpecialists)]
        
    def append_client(self, Client : Client):
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
        else:
            print('Queue is empty')
    
    def checkStatusEmployees(self):
        for emp in range(len(self.employees)):
            if self.employees[emp].status == 'free' and self.length != 0:
                self.employees[emp].currentClient = self.dequeue()
                self.employees[emp].change_status()
                #ZAKTUALIZUJ CZAS POZOSTALY PRACOWNIKOWI
                
                
                
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


#zakladam 4 specjalistów konta, 3 kredyty, 2 pozyczki i 2 kryzys
#20 procent szans że klient wybrał źle kolejkę

class Simulation:
    
    def __init__(self, day : str):
        self.queueAccount = Queue(4)
        self.queueCredit = Queue(3)
        self.queueLoan = Queue(2)
        self.queueCrisis = Queue(2)
        
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            self.flowOfClients = 4
            self.start_time = datetime.now().replace(microsecond=0, second=0, minute=0, hour=8)  
        else:
            self.flowOfClients = 8
            self.startTime = datetime.now().replace(microsecond=0, second=0, minute=0, hour=9)  
    
    def check_case_of_client(self, client : Client):
        if client.case == 'personal account':
            self.queueAccount.append_client(client)
        elif client.case == 'credits':
            self.queueCredit.append_client(client)
        elif client.case == 'loans':
            self.queueLoan.append_client(client)
        else:
            self.queueCrisis.append_client(client)
            
    def simulate(self, timeToSimulate):
        current = 0
        now = self.startTime
        while current < timeToSimulate:
            timeToNextClient = random.expovariate(self.flowOfClients)
            
            #arrival of client, append to the queue
            now = self.startTime + timedelta(minutes=current)
            client = Client(now)
            self.check_case_of_client(client)
            
            for queue in (self.queueAccount, self.queueCredit, self.queueLoan, self.queueCrisis):
                pass
            
            current += timeToNextClient