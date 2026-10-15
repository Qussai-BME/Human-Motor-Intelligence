# Dataset Source Notes

> These notes document public source checks performed while seeding the registry. They are **metadata evidence only**. No dataset files were downloaded, stored, or included in this repository.

## NinaPro Registry Evidence

The official [NinaPro dataset portal](https://ninapro.hevs.ch/) describes NinaPro as a publicly available multimodal database and lists the constituent database characteristics. Its table identifies DB2 as 40 subjects with 49 movements and a 12-electrode Delsys Trigno sEMG setup; DB3 as 11 amputee participants with 49 movements and a 12-electrode Delsys Trigno sEMG setup; and DB7 as 20 intact and 2 amputee participants with six movements and a 12-electrode Delsys Trigno sEMG setup. The portal asks users to cite the corresponding dataset article. Registry cards therefore record the public official source and an access/citation condition, while leaving all raw data external. [1]

## BCI Competition IV-2a Registry Evidence

The official [BCI Competition IV page](https://www.bbci.de/competition/iv/) describes dataset 2a as a four-class cued motor-imagery EEG resource containing left-hand, right-hand, feet, and tongue imagery; 22 EEG plus three EOG channels; 250 Hz sampling; and nine subjects. Its download section requires agreement to reference/cite the originating group and applicable paper. The registry therefore records it as an externally accessed, citation-conditioned EEG dataset rather than embedding a copy. [2]

## Registry Governance Consequence

The source pages do not substitute for a study-specific data-access audit. Every real-data run must record the precise accessed dataset version, acquisition date, access terms, local authorized location, canonicalization decisions, and citation. A synthetic fixture, even if structurally similar, cannot become a benchmark result.

## References

[1] [NinaPro — Official Dataset Portal](https://ninapro.hevs.ch/)

[2] [BCI Competition IV — Official Dataset 2a Description](https://www.bbci.de/competition/iv/)

## NinaPro DB2 Technical Detail

The official [NinaPro DB2 instructions](https://ninapro.hevs.ch/instructions/DB2.html) state that DB2 uses 12 Delsys Trigno electrodes and sEMG sampled at 2 kHz. They describe 40 intact subjects and 49 hand movements, with raw variables and placement context. The registry uses these values for DB2 and treats every downstream preprocessing/windowing choice as a protocol-level declaration, not as implicit dataset metadata. [3]

[3] [NinaPro DB2 — Official Instructions](https://ninapro.hevs.ch/instructions/DB2.html)

## Additional Registry Evidence

The official [NinaPro DB3 instructions](https://ninapro.hevs.ch/instructions/DB3.html) describe 11 transradial amputee participants, up to 12 Delsys Trigno sEMG channels, up to 49 movements plus rest, and 2 kHz sEMG sampling. The official [NinaPro DB7 instructions](https://ninapro.hevs.ch/instructions/DB7.html) describe 20 intact and two amputee participants, 12 Delsys Trigno IM sensors, 2 kHz sEMG sampling, and an explicit class-availability limitation for one amputee participant. [4] [5]

The [WAY-EEG-GAL Figshare collection](https://doi.org/10.6084/m9.figshare.c.988376.v2) describes 12 participants and 3,936 grasp-and-lift trials with 32 EEG channels, five EMG channels, event times, kinematics, and force/torque measures. This confirms it is a useful later multimodal research dataset, but it does not itself justify an EEG/EMG benchmark protocol or performance claim. [6]

The official [MIT-BIH Arrhythmia Database v1.0.0](https://doi.org/10.13026/C2F305) page states that the database is freely available under the Open Data Commons Attribution License v1.0 and includes 48 half-hour two-channel ambulatory ECG excerpts from 47 subjects sampled at 360 Hz. [7]

[4] [NinaPro DB3 — Official Instructions](https://ninapro.hevs.ch/instructions/DB3.html)

[5] [NinaPro DB7 — Official Instructions](https://ninapro.hevs.ch/instructions/DB7.html)

[6] [WAY-EEG-GAL — Springer Nature Figshare Collection](https://doi.org/10.6084/m9.figshare.c.988376.v2)

[7] [MIT-BIH Arrhythmia Database v1.0.0 — PhysioNet](https://doi.org/10.13026/C2F305)
