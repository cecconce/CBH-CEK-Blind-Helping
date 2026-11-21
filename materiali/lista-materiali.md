# Lista materiali

Aggiornata il 21 novembre 2026. I materiali del progetto sono acquistati dalla scuola. Prezzi indicativi, da preventivare.

Stato: ✅ disponibile · 📦 ordinato / in arrivo · 🛒 nella richiesta d'acquisto · 🤔 da valutare

## Già disponibile

| Stato | Componente | Q.tà | Uso | Note |
|---|---|---|---|---|
| ✅ | Arduino UNO Q | 1 | Scheda principale | |
| ✅ | Hub USB-C | 1 | Monitor, tastiera, alimentazione | |
| ✅ | Modulino Distance (VL53L4CD) | 1 | Zona vicina | Portata ~1,2 m, cono 18° |
| ✅ | Modulino Vibro | 1 | Feedback tattile | |
| ✅ | Sensore ToF VL53L1X (modulo rosso «VL53LXX») | 3 | Piano di riserva senza camera: uno 22° in alto, uno dritto, uno 30° in basso | Del referente. Portata nominale 4 m, cono 27°. Pin da saldare; stesso indirizzo I²C dei Modulino Distance (serve il Modulino Hub o il pin SHUT) |
| ✅ | Webcam Logitech C270 | 1 | Riconoscimento oggetti (prototipo versione 3) | Non misura la profondità |
| ✅ | Power bank UGREEN Nexode 20.000 mAh 130 W | 1 | Prove in laboratorio | Del referente |
| 📦 | Modulino Movement (IMU) | 1 | Fermo / cammina; correzione dell'angolo del busto per il TF-Luna | |

## Richiesta d'acquisto anno 1 (modulo scuola del 21/11/2026)

Un prototipo completo. Totale stimato circa 450–550 €. Fornitori proposti: RS Components Italia, Mouser, Robot-Italy, Arduino Store.

| Stato | n. | Componente | Produttore | Codice | Q.tà | Uso |
|---|---|---|---|---|---|---|
| 🛒 | 1 | Arduino UNO Q 2 GB / 16 GB | Arduino | ABX00162 | 1 | Scheda del prototipo |
| 🛒 | 2 | Camera di profondità con IA OAK-D Lite (fuoco fisso) | Luxonis | OAK-D-Lite-FF | 1 | Sensore principale: ostacoli entro 2 m. Montata orizzontale sul petto |
| 🛒 | 3 | Modulino Distance (ToF 0–1,2 m) | Arduino | ABX00102 | 4 | Zona vicina, puntati in alto e in basso |
| 🛒 | 4 | Modulino Hub (multiplexer I²C 8 canali) | Arduino | ABX00100 | 1 | Più sensori con lo stesso indirizzo I²C |
| 🛒 | 5 | Modulino Movement (IMU 6 assi) | Arduino | ABX00101 | 1 | Movimento della persona, angolo del busto |
| 🛒 | 6 | Modulino Vibro | Arduino | ABX00130 | 2 | Vibrazione sinistra / destra |
| 🛒 | 7 | Modulino Buttons | Arduino | ABX00110 | 1 | Comandi |
| 🛒 | 8 | Modulino Buzzer | Arduino | ABX00108 | 1 | Avvisi sonori |
| 🛒 | 9 | Hub USB-C con ingresso USB-PD ≥ 60 W e porte USB-A | a scelta | — | 1 | Alimenta UNO Q e camera |
| 🛒 | 10 | Power bank 20.000 mAh USB-C PD 87 W | Anker | A1383011 | 1 | Alimentazione indossabile |
| 🛒 | 11 | Cavo USB-C/USB-C 24 pin, 0,5 m | a scelta | — | 2 | |
| 🛒 | 12 | Kit cavi Qwiic | SparkFun | KIT-15081 | 1 | Catena dei Modulino |
| 🛒 | 13 | LiDAR ToF TF-Luna 0,2–8 m | Benewake | TF-Luna | 1 | Gradini in discesa: puntato a terra circa 1,5 m davanti ai piedi |
| 🤔 | 14 | Riga libera: eventuale Arduino USB Camera | Arduino | TPX00246 | 1 | Piano B se la OAK-D Lite non funziona sulla UNO Q |

Prezzi indicativi (nov. 2026): OAK-D Lite circa 189–220 €; Modulino circa 11 € + IVA l'uno; TF-Luna circa 36 €.

## Da valutare

| Stato | Componente | Q.tà | Uso | Note |
|---|---|---|---|---|
| 🤔 | Sensore ToF VL53L7CX 8×8 | 1 | Zona vicina a griglia, campo visivo largo | ~25 €, non acquistato |
| 🤔 | Modulo audio (es. DFPlayer Mini) o cuffie a conduzione ossea | 1 | Ritorno vocale | Da decidere: audio da Linux o modulo dedicato |

## Giubbino (reparto Moda) — anno 2

| Stato | Componente | Q.tà | Note |
|---|---|---|---|
| 🤔 | Gilet base tipo alta visibilità | da definire | |
| 🤔 | Tasche / supporti per sensori e scheda | da definire | Cartamodello a cura del reparto Moda |
| 🤔 | Supporti stampati in 3D per i sensori | da definire | Devono fissare gli angoli di puntamento dei sensori |

## Non più previsti

- Sensori a ultrasuoni HC-SR04 e ToF VL53L5CX: tolti dal progetto.
- Telecamera di profondità Orbbec Astra: sostituita dalla OAK-D Lite.

## Storico acquisti

| Data | Cosa | Stato |
|---|---|---|
| 2026-10 | Kit UNO Q + hub + Modulino Distance + Vibro | Arrivato |
| 2026-10 | Modulino Movement | Ordinato |
| 2026-11-21 | Richiesta d'acquisto anno 1 (13 righe) | Compilata, da consegnare al DSGA |
