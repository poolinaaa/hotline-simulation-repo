import time
import random
from queue import Queue

class KolejkaSymulacyjna:
    def __init__(self):
        self.kolejka = Queue()

    def naplyw_klientow(self, czas_symulacji, lambda_param):
        czas_plywu = 0
        while czas_plywu < czas_symulacji:
            # Generowanie czasu między klientami z rozkładem wykładniczym
            czas_do_nastepnego_klienta = random.expovariate(lambda_param)

            # Symulacja napływu klienta
            now = time.strftime("%H:%M:%S")
            print(f"{now} - Nowy klient! Czas do następnego klienta: {czas_do_nastepnego_klienta:.2f} sekundy")

            # Dodanie klienta do kolejki
            self.kolejka.put(now)

            # Poczekaj przed napływem kolejnego klienta
            time.sleep(czas_do_nastepnego_klienta)

            czas_plywu += czas_do_nastepnego_klienta

    def obsluga_klientow(self):
        while not self.kolejka.empty():
            # Pobierz klienta z kolejki
            klient = self.kolejka.get()

            # Symulacja obsługi klienta
            now = time.strftime("%H:%M:%S")
            print(f"{now} - Obsługa klienta: {klient}")

            # Symulacja czasu obsługi (możesz dostosować czas w zależności od potrzeb)
            time.sleep(1)

if __name__ == "__main__":
    kolejka_symulacyjna = KolejkaSymulacyjna()

    # Symulacja napływu klientów z rozkładem wykładniczym (lambda_param = 0.2)
    kolejka_symulacyjna.naplyw_klientow(czas_symulacji=30, lambda_param=0.2)

    # Symulacja obsługi klientów
    kolejka_symulacyjna.obsluga_klientow()
