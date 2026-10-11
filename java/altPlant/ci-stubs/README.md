Compile-only stubs of the few `javax.baja` classes that `altPlant-rt` uses, so CI can type-check the
components without the Tridium jars (they are licensed and not in this repository).
Signatures follow the Niagara 4 API; the bodies do nothing. The real build is still `gradlew build`
inside a Niagara 4.15 installation (see `../README_TH.md`). Do not put these classes on a station.
