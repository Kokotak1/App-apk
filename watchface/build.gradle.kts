plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred25eco"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred25eco"
        minSdk = 33
        targetSdk = 36
        versionCode = 12
        versionName = "2.5"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
