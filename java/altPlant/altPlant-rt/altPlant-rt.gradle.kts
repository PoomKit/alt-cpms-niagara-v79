plugins {
  id("com.tridium.niagara-module")
  id("com.tridium.niagara-signing")
  id("com.tridium.niagara-annotation-processors")
  id("com.tridium.convention.niagara-home-repositories")
}

description = "ALT Reference V7.9 plant components (expansion supervisor, zone aggregator)"

moduleManifest {
  moduleName.set("altPlant")
  runtimeProfile.set("rt")
  vendor.set("ALT")
}

dependencies {
  nre(":nre")
  api(":baja")
}
