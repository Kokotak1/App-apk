plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred20"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred20"
        minSdk = 33
        targetSdk = 36
        versionCode = 7
        versionName = "2.0"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
