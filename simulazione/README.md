# Simulazione di fattibilità CBH — 21 novembre 2026

Simulazione software per capire se la componentistica scelta può soddisfare il requisito "cane guida": ostacoli entro 2 m, fino a 2 m di altezza e 1,5 m di larghezza.

**Esito: con la camera di profondità il sistema può funzionare; con i soli ToF + TF-Luna no.**

## Metodo
- Ray casting dei coni dei sensori contro 10 ostacoli tipo, con i sensori sul petto a 1,30 m (`cbh_cov.py`).
- Monte Carlo sui tempi di reazione, sul gradino in discesa e sull'autonomia (`cbh_sim.py`).
- Dati dei sensori di targa, non misurati: i risultati vanno confermati sul prototipo.

## Spazio d'arresto (95% dei casi)
| Velocità | Spazio d'arresto |
|---|---|
| 0,6 m/s | 0,7 m |
| 1,0 m/s (passo normale) | 1,3 m |
| 1,4 m/s (passo svelto) | 2,0 m |

Un allarme a 2 m basta fino a 1,4 m/s. Un allarme a 1,2 m (solo Modulino Distance) basta fino a circa 1,0 m/s.

## Copertura degli ostacoli
| Configurazione | Risultato |
|---|---|
| Con camera OAK-D Lite | Tutti gli ostacoli visti ad almeno 2,1 m, quindi in tempo |
| Solo 4 ToF + TF-Luna | In tempo solo il muro; persona vista a circa 1 m; paletto, sedia e cordolo mai visti |

- Palo sottile (5 cm): il ToF lo sente solo a circa 0,5 m, perché riempie poco il cono da 18°.
- Ultimo metro: la camera perde gli oggetti bassi (paletto e sedia sotto 1,15 m). Il software deve ricordare gli ostacoli già visti.
- I ToF puntati in alto e in basso portano la copertura della zona vicina dal 52% al 69–74%.

## Inclinazione della camera
| Inclinazione | Vede il pavimento da | Altezza vista a 1,3 m | Ostacoli alla testa (1,7–2 m) |
|---|---|---|---|
| Orizzontale | 2,35 m | 2,02 m | visti fino a 0,7–0,8 m |
| 15° in basso | 1,35 m | 1,62 m | persi sotto 1,6–1,75 m |

## Gradino in discesa
- La camera distingue un gradino da 10 cm solo a circa 1,0 m (tardi); uno da 15 cm a 2,1 m.
- TF-Luna puntato a terra a 1,5 m: il gradino da 10 cm produce un salto di 15 cm, contro 6 cm di rumore del sensore.
- L'oscillazione del busto di ±4° crea un falso salto di 16 cm; corretta a ±1° con l'IMU scende a 4 cm.

## Alimentazione e bus
- Consumo stimato 7–10,5 W, autonomia 6–9 h con il power bank da 72 Wh (ipotesi sui consumi di UNO Q e camera, da misurare).
- Giro I²C dei 4 ToF attraverso il Modulino Hub: circa 10 ms, non è un collo di bottiglia.

## Decisioni prese
- **OAK-D Lite**: sul petto, orizzontale.
- **TF-Luna**: puntato a terra, circa 1,5 m davanti ai piedi (inclinazione di circa 41°), in coppia con il Modulino Movement.
- **4 Modulino Distance**: due verso l'alto (circa +50°) e due verso il basso (circa −40° e −60°). Angoli di partenza, da ritoccare sul prototipo.

## Cosa la simulazione non dice
- Se la OAK-D Lite funziona sull'UNO Q (USB, container di App Lab): è il primo collaudo da fare.
- Il comportamento dei ToF al sole, su vetro e su superfici scure.
- Se la vibrazione si sente attraverso il tessuto del giubbino.

## Da misurare sul prototipo
- Consumi reali di UNO Q e camera.
- Portata dei ToF su ostacoli sottili e scuri.
- Rilevamento del gradino con TF-Luna + IMU.

## Aggiunta: piano senza camera con 2 VL53L1X (`cbh_l1x.py`)
Il referente ha due moduli VL53L1X (cono di 27°, portata nominale 4 m). Aggiunti ai 4 Modulino Distance e al TF-Luna, senza camera:

| Ostacolo | Senza VL53L1X | Con 2 VL53L1X (uno 12° in alto, uno 20° in basso) |
|---|---|---|
| Persona | 0,35 m | 2,10 m |
| Muro | 1,50 m | 2,50 m |
| Bordo tavolo | 0,70 m | 1,45 m |
| Transenna a 1 m | 0,40 m | 1,15 m (tardi) |
| Paletto, sedia, cartello alto, ramo | mai o tardi | mai o tardi |

- Ostacoli visti in tempo (allarme ad almeno 1,29 m): da 2 su 10 a 4 su 10.
- Con luce forte la portata può scendere verso 1,3 m e il vantaggio sparisce (2 su 10).
- Conclusione: i VL53L1X migliorano il piano di riserva su persone e pareti, ma non sostituiscono la camera di profondità.

