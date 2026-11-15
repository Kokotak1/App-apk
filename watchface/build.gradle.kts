plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred4"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred4"
        minSdk = 33
        targetSdk = 36
        versionCode = 2
        versionName = "1.5"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
