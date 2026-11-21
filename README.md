# ETA – CBH «CEK Blind Helping»

Giubbino sensorizzato (Electronic Travel Aid) per la mobilità autonoma di persone con disabilità visiva.
Progetto PTOF a.s. 2026/2027 – ISIS «Lino Zanussi» di Pordenone, in collaborazione con UICI.

Docente referente: Prof. Pierluigi Ceccon
Studenti coinvolti: IPSIA (elettronica / MAT) e reparto Moda (confezione del giubbino)

## L'idea

Il cane guida si ferma davanti a un ostacolo entro circa **1 m**, con una copertura fino a **2 m in altezza** e **1,5 m in larghezza** (indicazioni del tecnico UICI Corrado Bortolin).
Non tutti possono avere un cane guida: il giubbino CBH vuole sorvegliare lo stesso volume davanti alla persona e avvisarla con **vibrazioni** e **messaggi vocali**.

Requisito chiave: rilevare ostacoli **al massimo entro 2 m** (non serve vedere lontano).

## Architettura (prototipo attuale)

| Parte | Componente | Ruolo |
|---|---|---|
| Scheda | Arduino UNO Q | Microcontrollore (STM32U585) per sensori e vibrazione in tempo reale; Linux (QRB2210) per webcam, riconoscimento oggetti, audio |
| Distanza | Modulino Distance (ToF) | Ostacolo frontale vicino |
| Distanza a zone | VL53L5CX 8×8 | Copertura più ampia del volume frontale |
| Feedback tattile | Modulino Vibro | Vibrazione proporzionale alla vicinanza |
| Visione | Webcam Logitech C270 | Riconoscimento oggetti (lato Linux) |
| Movimento | Modulino Movement (in arrivo) | Riconoscere fermo / cammina, adattare gli avvisi |

I Modulino si collegano in catena con cavi **Qwiic** al connettore della UNO Q, senza saldature.

## Struttura del repository

```
docs/
  decisioni.md        registro delle decisioni prese (con data)
  diario/             un file per ogni settimana di sviluppo (AAAA-Wnn.md)
materiali/
  lista-materiali.md  cosa c'è, cosa è ordinato, cosa comprare
firmware/             sketch Arduino e app per Arduino App Lab
simulazione/          simulazione di fattibilità (risultati + script Python)
```

## Aggiornamento settimanale

Ogni fine settimana vengono aggiornati il diario, le decisioni e la lista dei materiali da acquistare.
