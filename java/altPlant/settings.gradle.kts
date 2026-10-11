// Niagara 4.15 multi-project build (same layout as Workbench > Tools > New Module)
pluginManagement {
  repositories {
    maven(url = "${System.getProperty("niagara_home") ?: System.getenv("NIAGARA_HOME")}/etc/m2/repository")
    gradlePluginPortal()
  }
}
plugins {
  id("com.tridium.settings.conventions") version "7.15.0"   // use the version shipped in <niagara_home>/etc/m2
}
rootProject.name = "altPlant"
include("altPlant-rt")
