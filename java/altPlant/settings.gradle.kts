// Niagara 4.15 multi-project build (same layout as Workbench > Tools > New Module)
pluginManagement {
  // version of the Tridium gradle plugins shipped in <niagara_home>/etc/m2 - set in gradle.properties
  val niagaraGradlePluginVersion: String by settings
  repositories {
    maven(url = "${System.getProperty("niagara_home") ?: System.getenv("NIAGARA_HOME")}/etc/m2/repository")
    gradlePluginPortal()
  }
  plugins {
    id("com.tridium.settings.conventions") version niagaraGradlePluginVersion
  }
}
plugins {
  id("com.tridium.settings.conventions")
}
rootProject.name = "altPlant"
include("altPlant-rt")
