# Memory Map

| Addr  | Notes                      |
| ----- | -------------------------- |
| $0000 | Fixed ROM Start            |
| $1fff | Fixed ROM End              |
| $2000 | Banked ROM Start           |
| $3fff | Banked ROM End             |
| $4000 | Banked RAM Start           |
| $5fff | Banked RAM End             |
| $6000 | Fixed RAM Start            |
| $8000 | Frame Buffer Start         |
| $bfff | Frame Buffer End           |
| $fbff | Fixed RAM End              |
| $fc00 | ROM Bank Select (IO Start) |
| $fc01 | RAM Bank Select            |
| $fc02 | Graphics Mode Toggle       |
| $fc03 | Graphics Intensity         |
| $ffff | IO End                     |