# Registro delle decisioni

Ogni decisione ha una data e una breve motivazione. Le nuove vanno in fondo.

| Data | Decisione | Motivazione / note |
|---|---|---|
| 2026-09 | Progetto proposto come PTOF 2026/27, con IPSIA (elettronica) e Moda (giubbino) | Collaborazione con UICI |
| 2026-09 | Lista materiali basata sullo scenario più costoso della tabella costi | Più prototipi e ricambi |
| 2026-09 | Scheda del progetto: **Arduino UNO Q** (niente Raspberry Pi come scheda) | AI a bordo + microcontrollore in tempo reale; periferiche anche di altre marche |
| 2026-10 | Sensori e vibrazione su catena **Qwiic / Modulino** | Niente saldature, 3,3 V nativi, adatto alla demo |
| 2026-10 | Portata massima di interesse: **2 m** | Il volume da proteggere è 1 × 1,5 × 2 m; sensori a lunga portata (es. TF-Luna) non servono |
| 2026-10 | Divisione dei compiti: MCU = sensori + vibrazione; Linux = webcam, riconoscimento, audio | Tempi deterministici sul microcontrollore |
| 2026-10 | Acquisto del **Modulino Movement** | Adattare gli avvisi a fermo / cammina |
| 2026-10 | Per la demo al collegio si resta sulla versione 3 (Distance + Vibro + webcam) | La versione con Movement sarà una nuova app (test-cbh-4) |
| 2026-11 | Preventivo ~3.000 € spalmato dalla dirigente su due anni | I materiali sono acquistati dalla scuola |
| 2026-11-21 | Avviato questo repository con aggiornamento settimanale | Storico dello sviluppo e degli acquisti |
| 2026-11-21 | Simulazione software di fattibilità (vedi `simulazione/`) | Esito: con la camera di profondità il sistema può funzionare; con i soli ToF + TF-Luna no |
| 2026-11-21 | Camera di profondità **OAK-D Lite** montata **orizzontale** sul petto | A 1,3 m vede fino a 2,02 m di altezza (ostacoli alla testa); inclinata di 15° li perderebbe sotto 1,6–1,75 m |
| 2026-11-21 | **TF-Luna** rientra nel progetto, puntato a terra circa 1,5 m davanti ai piedi, in coppia con il Modulino Movement | Sostituisce la nota di ottobre: non serve per la portata, serve per i gradini in discesa (salto di 15 cm per un gradino da 10 cm); l'IMU corregge l'oscillazione del busto |
| 2026-11-21 | 4 **Modulino Distance** puntati in alto e in basso (circa +50° e −40/−60°), non in avanti | Coprono la zona vicina che la camera non inquadra: dal 52% al 69–74% |
