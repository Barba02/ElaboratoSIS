## Testing automatico
Nelle cartelle _istanze_ e _random_ si trovano dei test scritti in python per verificare il corretto funzionamento del circuito.<br/>
I test si basano sull'esecuzione di sis in un sottoprocesso e il confronto tra gli output restituiti e quelli attesi.<br/>
**Requisiti**<br/>
-> Entrambi i test devono essere eseguiti su macchina Linux con sis installato<br/>
-> Per non causare errori all'esecuzione dei test è richiesto che non vengano spostati o rinominati i file del progetto<br/>
**Avviso**<br/>
I test creano dei file durante l'esecuzione che alla fine non vengono cancellati dato che potrebbe esserne utile la visione.
### Istanze
Il test verifica alcune istanze fornite dal prof. Stefano Centomo per i diversi casi d'uso e per latenze diverse.<br/>
Per raggiungere il punteggio massimo è necessario che il circuito passi l'istanza 5, una tra le istanze 1 e 2, una tra le istanze 3 e 4 e una tra le istanze 6 e 7.<br/>
! Eseguire da terminale con ```python3 istanze.py``` dopo essersi posizionati nella cartella _istanze_<br/>
### Random
Il test crea randomicamente degli input da dare a sis e gli output attesi con quegli input,
successivamente esegue sis e ne rileva gli output per paragonarli a quelli attesi.<br/>
È possibile scegliere quanti test eseguire e quanti input generare per ogni test inserendo i due valori come parametri da linea di comando.<br/>
! Eseguire da terminale con ```python3 random_test.py num_test num_input``` dopo essersi posizionati nella cartella _random_<br/>
