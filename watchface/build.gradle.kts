plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred2"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred2"
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "1.2"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
