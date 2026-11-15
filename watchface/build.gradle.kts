plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred8"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred8"
        minSdk = 33
        targetSdk = 36
        versionCode = 5
        versionName = "1.8"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
