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
| 2026-11-21 | Ritorno vocale via **Bluetooth** integrato nella UNO Q, senza modulo audio dedicato | La scheda ha già Wi-Fi 5 e Bluetooth 5.1; cuffie a conduzione ossea per lasciare libere le orecchie. Da verificare sul prototipo |
| 2026-11-21 | Cuffie Bluetooth a conduzione ossea di marca (Creative Outlier Free+, alt. Shokz OpenMove) nella richiesta | Lasciano libere le orecchie; modelli senza marca da 30–40 € scartati (nessuna recensione indipendente, venditore terzo) |
| 2026-11-22 | Tutti i sensori I²C collegati su **Qwiic** | Collegamenti senza saldature e uniformi; i 3 VL53L1X personali si collegano con cavi Qwiic–jumper femmina (CAB-17261) dopo aver saldato la strip di pin |
| 2026-11-22 | Richiesta anno 1 estesa a 18 righe: 3 VL53L1X Qwiic (SEN-14722), 3 cavi CAB-17261, Arduino USB Camera (TPX00246) come piano B, alimentatore USB-C 45 W | Piano di riserva senza camera di profondità (test simulato); la USB Camera è supportata ufficialmente in App Lab |
| 2026-11-22 | UNO Q 4 GB (ABX00173), hub, USB Camera e alimentatore presi nel bundle Black Friday dell'Arduino Store | Scheda scontata del 40%: ordine Arduino 204,84 € invece di circa 265,50 €. Se i tempi della procedura PA non lo permettono, stesse righe a listino da RS o Mouser |
| 2026-11-22 | Il materiale comprato personalmente dal referente resta suo e non riduce la richiesta della scuola | La scuola per ora non ha fondi; gli acquisti personali servono a iniziare subito le prove |
| 2026-11-22 | Lavoro sul prototipo affidato a un gruppo ristretto di 4 studenti della 3A, selezionati con un test | Compiti: sito, GitHub aperto, realizzazione a step (un sensore alla volta), saldatura VL53L1X, software |
