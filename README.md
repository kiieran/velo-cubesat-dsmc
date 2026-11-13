# DSMC Drag Study of a VLEO CubeSat

Rarefied-flow (DSMC) study of how nose geometry and surface materials affect drag on a 3U CubeSat in very low Earth orbit (~400 km), using [SPARTA](https://github.com/sparta/sparta). The method is validated against free-molecular theory and against the University of Manchester's ADBSat tool on a reconstructed model of the SOAR satellite. It is then used to compare seven nose designs that all fit the standard 3U launch envelope.

## Key results

- **Validated workflow:** within 0.3% of analytical free-molecular theory, and within 3% of Manchester's ADBSat panel-method tool on a reconstructed SOAR model.
- **Shape alone does little:** with realistic (diffuse) surfaces, the best nose shape cuts drag by 22%, and it gives up a third of the internal volume to do it.
- **A low-drag coating only pays off once the nose is shaped:** coating the whole of SOAR's flat-fronted shape *raises* drag by 7%. On shaped noses, the same coating cuts drag by up to 56% with an improved material (CLL, accommodation 0.5), and by up to 70% with an ideal specular one.
- **Why:** a reflective coating reduces drag only on surfaces angled less than ~46° to the flow, and increases it on steeper, forward-facing ones. A shaped nose puts almost all of its surface below that angle.
- **Best trade-off:** the square blunt bullet keeps 95% of the internal volume and, fully coated with the improved material, cuts drag by 39%.
- **Effects a panel method misses:** DSMC captures thermal shadowing of the fins by the body, and molecules reflected from the body onto the fins.

![Drag comparison](figures/drag_comparison.png)

## The designs

Every body fits inside the 3U envelope (100 × 100 × 366 mm), with its rear face in the same place. The four fins, the flow conditions and the reference area are identical in every case, so only the body changes. Click a name to open the 3D model in GitHub's viewer.

| | | | |
|:---:|:---:|:---:|:---:|
| <img src="figures/designs/SOAR.png" width="190"> | <img src="figures/designs/SOAR (Obtuse Wedge).png" width="190"> | <img src="figures/designs/SOAR (Wedge).png" width="190"> | <img src="figures/designs/SOAR (Acute Wedge).png" width="190"> |
| [**SOAR baseline**](geometry/soar_body.stl)<br>3.47 L · flat front + INMS | [**Obtuse wedge**](geometry/wedge_obtuse.stl)<br>3.52 L · ~120° apex | [**Wedge**](geometry/wedge.stl)<br>3.41 L · ~90° apex | [**Acute wedge**](geometry/wedge_acute.stl)<br>2.73 L · ~30° apex |
| <img src="figures/designs/SOAR (Square Blunt Bullet).png" width="190"> | <img src="figures/designs/SOAR (Square Pointed Bullet).png" width="190"> | <img src="figures/designs/SOAR (Round Blunt Bullet).png" width="190"> | <img src="figures/designs/SOAR (Round Pointed Bullet).png" width="190"> |
| [**Square blunt bullet**](geometry/square_blunt_bullet.stl)<br>3.31 L | [**Square pointed bullet**](geometry/square_pointed_bullet.stl)<br>2.77 L | [**Round blunt bullet**](geometry/round_blunt_bullet.stl)<br>2.68 L | [**Round pointed bullet**](geometry/round_pointed_bullet.stl)<br>2.33 L |

## Results

Total drag coefficient with the fins flat (A_ref = 0.1125 m²). Each wall model is applied to every surface of the satellite, fins included. Percentages are against SOAR with diffuse walls.

| Design | Volume | Diffuse | CLL 0.5 | Specular |
|---|---|---|---|---|
| SOAR baseline | 3.47 L | 0.395 | 0.421 (+7%) | 0.439 (+11%) |
| Obtuse wedge | 3.52 L | 0.395 (0%) | 0.360 (−9%) | 0.350 (−11%) |
| Wedge | 3.41 L | 0.390 (−1%) | 0.296 (−25%) | 0.261 (−34%) |
| Acute wedge | 2.73 L | 0.361 (−9%) | 0.186 (−53%) | 0.114 (−71%) |
| Square blunt bullet | 3.31 L | 0.379 (−4%) | 0.240 (−39%) | 0.186 (−53%) |
| Square pointed bullet | 2.77 L | 0.357 (−10%) | 0.189 (−52%) | 0.121 (−69%) |
| Round blunt bullet | 2.68 L | 0.326 (−17%) | 0.224 (−43%) | 0.185 (−53%) |
| Round pointed bullet | 2.33 L | 0.310 (−22%) | 0.172 (−56%) | 0.117 (−70%) |

Statistical noise is about ±0.002 in C_D.

## Supplementary: partial coating

Because a reflective coating only helps below ~46°, drag could be reduced further by leaving the steepest surfaces uncoated. This was simulated (`scripts/tag_by_angle.py` splits each body by surface angle), but it is **not recommended**. Those steep, ram-facing surfaces (facing the direction of travel, into the oncoming atmosphere) receive the most atomic oxygen, so they are where a protective coating matters most. Leaving them bare would expose them to erosion and oxidation, and the loss of lifetime is likely to outweigh the drag saving.

Drag with the steep surfaces left bare and the rest coated (fins flat, CLL / specular), for comparison with full coating:

| Design | Fully coated | Steep surfaces bare | Drag saved by leaving them bare |
|---|---|---|---|
| SOAR | 0.421 / 0.439 | 0.307 / 0.272 | 27% / 38% |
| Obtuse wedge | 0.360 / 0.350 | 0.306 / 0.270 | 15% / 23% |
| Round blunt bullet | 0.224 / 0.185 | 0.213 / 0.168 | 5% / 9% |
| Square blunt bullet | 0.240 / 0.186 | 0.238 / 0.182 | 1% / 2% |
| Wedge, acute wedge, pointed bullets | – | – | 0% (no surface steeper than 46°) |

The saving is large only for flat or blunt fronts. On the shaped noses it is small or zero, which supports the main conclusion: shaping the nose lets the whole satellite be coated for protection while still gaining the full drag benefit.

## Method

| Item | Value |
|---|---|
| Solver | SPARTA DSMC, 10 MPI ranks on an Apple M4 Pro |
| Geometry | Onshape, exported as text STL in metres |
| Atmosphere | ~400 km, NRLMSIS 2.0 (Oct–Nov 2021, F10.7 = 85): 818 K, 7.67 km/s, n = 4.94 × 10¹³ m⁻³; 87.6% O, 7.5% He, 3.1% N₂, 1.9% N |
| Wall temperature | 300 K |
| Reference area | 0.1125 m² (half of SOAR's total surface area, as in Crisp et al. 2021) |
| Averaging | 3,000 fill steps, then forces averaged over 10,000 steps |

### Wall models

In free molecular flow, drag is set by what happens when a molecule hits the surface. The three conditions are:

- **Diffuse** (realistic): the molecule is re-emitted in a random direction at the wall temperature. Atomic oxygen adsorbs onto spacecraft surfaces and makes them behave this way.
- **CLL, accommodation 0.5** (improved material): the Cercignani–Lampis–Lord model, partway between diffuse and specular. In SPARTA it is `cll 300.0 0.5 0.5 1.0 1.0` (normal and tangential *energy* accommodation 0.5), which is σ_T = 0.293 in ADBSat's momentum convention. The value is illustrative, not measured.
- **Specular** (ideal): mirror reflection, a theoretical limit.

A reflective surface roughly doubles the drag on a face-on surface, but greatly reduces it at grazing angles. A Monte Carlo calculation of each wall model puts the crossover at about **46°** for these conditions. This is why coating helps shaped noses but not SOAR's flat front.

### SOAR reconstruction

The SOAR model is a reconstruction from published data (Crisp et al. 2021, Table 1). The fin dimensions were not published. They were inferred from the total surface area, a fit to the published drag curves and the published images: 285 × 60 × 2 mm, with an assumed 60 mm INMS.

## Validation

| Step | Comparison | Agreement |
|---|---|---|
| 1 | Sphere and flat plate (diffuse, specular, CLL) vs analytical free-molecular solutions | within 0.3% |
| 2 | Reconstructed SOAR, 0–90° fin sweep vs ADBSat on the same geometry | within 3% |

![DSMC validation](figures/dsmc_validation.png)

The 2–3% that DSMC sits below ADBSat grows with fin angle. This is consistent with two effects that a panel method leaves out: the body shadowing the fin roots from thermally drifting molecules, and molecules reflected off the fins onto the body.

Both DSMC and ADBSat sit a near-constant 0.17–0.20 above the reference curves in Crisp et al. (2021, Fig. 10), while matching how drag changes with fin angle. A constant offset points to a difference in the baseline geometry used for those curves rather than in the aerodynamic modelling. Resolving it needs that geometry.

## Limitations

- Results are for one altitude and solar condition. C_D varies by about 0.5% across the plausible solar range.
- CLL 0.5 is an illustrative "improved material". Real surfaces under atomic oxygen are typically closer to diffuse.
- The SOAR fin and INMS dimensions are estimates.
- The design comparison uses two fin angles (0° and 90°), not a full sweep.
- Coatings are modelled only through their gas–surface interaction. Erosion, oxidation, and any change in accommodation as a coating ages are not modelled.
- No flight data has been compared, because SOAR's flight drag results are not yet public.

## Repository structure

```
figures/        result figures and design renders
geometry/       STL files for every body and the four fins
cases/          SPARTA input files, wall-model files, species data
scripts/        make_figures.py       – regenerates the figures
                tag_by_angle.py       – splits a body into steep (diffuse) and shallow (coated) triangles
                soar_to_obj.py        – converts the SOAR parts to OBJ for ADBSat
                run_soar_adbsat.m     – ADBSat fin sweep in MATLAB
```

## Status

Case files, geometry and post-processing scripts are being tidied for upload.

## References

- Crisp, N. H. et al. (2021). *In-orbit aerodynamic coefficient measurements using SOAR (Satellite for Orbital Aerodynamics Research).* Acta Astronautica 180, 85–99.
- Crisp, N. H. et al. (2022). *Experimental Results from the SOAR Mission.* 73rd International Astronautical Congress (IAC-22).
- Sinpetru, L. A. et al. (2022). *ADBSat: Verification and validation of a novel panel method for quick aerodynamic analysis of satellites.* Computer Physics Communications 275. [ADBSat on GitHub](https://github.com/nhcrisp/ADBSat)
- Plimpton, S. J. et al. (2019). *Direct Simulation Monte Carlo on petaflop supercomputers and beyond.* Physics of Fluids 31, 086101. [SPARTA](https://sparta.github.io)

## Acknowledgements

Post-processing and analysis scripts were developed with AI assistance (Claude, Anthropic). Geometry, simulations and interpretation are my own.
