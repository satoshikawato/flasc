[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/satoshikawato/flasc)
# flasc
inFLuenza Amino acid Substitution Caller

## Usage
### `--all` mode (default)
Displays every scanned site, including invariant ones
```sh
./mutation_scan.py -i HA.aligned.faa -d mutations.toml -t "HA" -q  UJS29065.1 --mode all
```
```sh
query   gene    coordinate      variant reference       residue note
UJS29065.1      HA      170     N158D   N       N       H3 numbering; mammalian adaptation
UJS29065.1      HA      172     T160A   T       A       H3 numbering; mammalian adaptation
UJS29065.1      HA      198     N186K   N       N       H3 numbering; synonym: N182K; mammalian adaptation (enhanced binding to alpha-2,6 SA)
UJS29065.1      HA      208     Q196R   Q       K       H3 numbering; synonym: Q192R (H5 numbering); mammalian adaptation (enhanced binding to alpha-2,6 SA)
UJS29065.1      HA      236     N224K   N       N       H3 numbering; mammalian adaptation
UJS29065.1      HA      205     K193R   K       N       H3 numbering; synonym: K189R (H5 numbering); mammalian adaptation
UJS29065.1      HA      238     Q226L   Q       Q       H3 numbering; synonym: Q222L (H5 numbering); mammalian adaptation
UJS29065.1      HA      240     G228S   G       G       H3 numbering; mammalian adaptation
UJS29065.1      HA      331     T318I   T       T       H3 numbering; mammalian adaptation
```
### `--variants` mode
Displays the line if the query sequence is different from the reference, even if the residue does not match that of the definition
```sh
./mutation_scan.py -i HA.aligned.faa -d mutations.toml -t "HA" -q  UJS29065.1 --mode variants
```
```sh
query   gene    coordinate      variant reference       residue note
UJS29065.1      HA      172     T160A   T       A       H3 numbering; mammalian adaptation
UJS29065.1      HA      208     Q196R   Q       K       H3 numbering; synonym: Q192R (H5 numbering); mammalian adaptation (enhanced binding to alpha-2,6 SA)
UJS29065.1      HA      205     K193R   K       N       H3 numbering; synonym: K189R (H5 numbering); mammalian adaptation
```
```sh
./mutation_scan.py -i HA.aligned.faa -d mutations.toml -t "HA" -q  UJS29065.1 --mode strict
```
### `--strict` mode
Displays only the variants that exactly match the predefined substituion(s)
```sh
query   gene    coordinate      variant reference       residue note
UJS29065.1      HA      172     T160A   T       A       H3 numbering; mammalian adaptation
```
## Output table
query	gene	coordinate	variant_id	ref	alt	note
|Col|Type  |Description                               |
|--:|:----:|:-----------------------------------------|
|1  |string|Query sequence name                       |
|2  |string|Query gene name                           |
|3  |int   |Query coordinate (1-based; closed)        |
|4  |string|Variant ID                                |
|5  |string|Reference (wildtype) residue              |
|6  |string|Query residue                             |
|7  |string|Notes (numbering scheme, synonyms, effects etc.)|


## Variant definition file 
The variants are defined in a [TOML](https://github.com/toml-lang/toml) format table
```toml
[PB2]
[PB2.E627K]
name = "E627K"
protein_id = "YP_308664.1"
gene_id = "PB2"
subtypes = "all"
wildtype = "E"
mutant = "K"
coordinate = "627"
reference_isolate = "A/goose/Guangdong/1/1996(H5N1)"
note = "mammalian adaptation"
citations = ["https://doi.org/10.1126/science.1062882",
            "https://doi.org/10.1128/jvi.67.4.1761-1764.1993"]
[PB2.D701N]
name = "D701N"
protein_id = "YP_308664.1"
gene_id = "PB2"
subtypes = "all"
wildtype = "D"
mutant = "N"
coordinate = "701"
reference_isolate = "A/goose/Guangdong/1/1996(H5N1)"
note = "mammalian adaptation"

# continued
```


