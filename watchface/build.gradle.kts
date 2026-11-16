plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred23eco"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred23eco"
        minSdk = 33
        targetSdk = 36
        versionCode = 10
        versionName = "2.3"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
